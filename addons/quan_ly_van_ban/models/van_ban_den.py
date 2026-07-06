from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
from . import ai_helper

class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa thông tin văn bản đến'
    _rec_name = 'ten_van_ban'

    so_van_ban_den = fields.Char("Số đến", required=True)
    so_hieu_van_ban = fields.Char("Số/Ký hiệu gốc", required=True)
    ten_van_ban = fields.Char("Tên văn bản", required=True)

    # Liên kết với model 'don_vi' và 'nhan_vien'
    don_vi_nhan_id = fields.Many2one('don_vi', string="Đơn vị nhận xử lý")
    nhan_vien_xu_ly_id = fields.Many2one('nhan_vien', string="Người xử lý chính")

    # Liên kết với Loại văn bản
    loai_van_ban_id = fields.Many2one('loai_van_ban', string="Loại văn bản")

    # Liên kết với Khách hàng & Số hóa tài liệu
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng liên quan")
    file_dinh_kem = fields.Binary("Tệp đính kèm")
    ten_file = fields.Char("Tên tệp")

    # Các trường tích hợp AI
    mo_ta = fields.Text("Nội dung/Mô tả văn bản")
    ai_summary = fields.Text("Tóm tắt từ AI", readonly=True)
    ai_suggested_employee_id = fields.Many2one('nhan_vien', string="Người xử lý đề xuất (AI)", readonly=True)
    ai_suggested_category_id = fields.Many2one('loai_van_ban', string="Loại văn bản đề xuất (AI)", readonly=True)
    ai_analysis_status = fields.Selection([
        ('not_analyzed', 'Chưa phân tích'),
        ('analyzed', 'Đã phân tích'),
        ('failed', 'Lỗi phân tích')
    ], string="Trạng thái phân tích AI", default='not_analyzed', readonly=True)

    def action_ai_analyze(self):
        for record in self:
            try:
                res, status = ai_helper.analyze_document_text(
                    self.env, 
                    record.ten_van_ban, 
                    record.mo_ta
                )
                
                update_vals = {
                    'ai_summary': res.get('summary', ''),
                    'ai_analysis_status': 'analyzed'
                }
                
                # Tìm category tương ứng
                if res.get('category'):
                    cat = self.env['loai_van_ban'].search([('ten_loai_van_ban', '=', res.get('category'))], limit=1)
                    if cat:
                        update_vals['ai_suggested_category_id'] = cat.id
                    else:
                        update_vals['ai_suggested_category_id'] = False
                else:
                    update_vals['ai_suggested_category_id'] = False
                        
                # Tìm nhân viên tương ứng
                if res.get('employee'):
                    emp = self.env['nhan_vien'].search([('ho_va_ten', '=', res.get('employee'))], limit=1)
                    if emp:
                        update_vals['ai_suggested_employee_id'] = emp.id
                    else:
                        update_vals['ai_suggested_employee_id'] = False
                else:
                    update_vals['ai_suggested_employee_id'] = False
                        
                record.write(update_vals)
                
                message = "Đã phân tích văn bản bằng AI thành công!"
                if status in ["mock", "fallback"]:
                    message += " (Chế độ mô phỏng - Chưa cấu hình Gemini API Key)"
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'AI Trợ Lý',
                        'message': message,
                        'sticky': False,
                        'type': 'success',
                    }
                }
            except Exception as e:
                record.write({'ai_analysis_status': 'failed'})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'AI Trợ Lý',
                        'message': f'Lỗi phân tích AI: {str(e)}',
                        'sticky': False,
                        'type': 'danger',
                    }
                }

    def action_apply_ai_suggestions(self):
        for record in self:
            vals = {}
            if record.ai_suggested_category_id:
                vals['loai_van_ban_id'] = record.ai_suggested_category_id.id
            if record.ai_suggested_employee_id:
                vals['nhan_vien_xu_ly_id'] = record.ai_suggested_employee_id.id
            if vals:
                record.write(vals)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'AI Trợ Lý',
                        'message': 'Đã áp dụng đề xuất của AI vào văn bản thành công!',
                        'sticky': False,
                        'type': 'success',
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'AI Trợ Lý',
                        'message': 'Không có đề xuất nào phù hợp để áp dụng.',
                        'sticky': False,
                        'type': 'warning',
                    }
                }


