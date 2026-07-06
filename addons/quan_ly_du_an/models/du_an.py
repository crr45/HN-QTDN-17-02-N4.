# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Thông tin dự án'
    _rec_name = 'ten_du_an'

    ma_du_an = fields.Char("Mã dự án", required=True)
    ten_du_an = fields.Char("Tên dự án", required=True)
    mo_ta = fields.Text("Mô tả dự án")
    ngay_bat_dau = fields.Date("Ngày bắt đầu")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Liên kết trực tiếp tới model 'nhan_vien' làm Quản lý và Thành viên (HRM data)
    nguoi_quan_ly_id = fields.Many2one('nhan_vien', string="Quản trị dự án", required=True)
    thanh_vien_ids = fields.Many2many(
        'nhan_vien', 
        'du_an_nhan_vien_rel', 
        'du_an_id', 
        'nhan_vien_id', 
        string="Thành viên dự án"
    )
    
    cong_viec_ids = fields.One2many('cong_viec_du_an', 'du_an_id', string="Danh sách công việc")

    _sql_constraints = [
        ('ma_du_an_unique', 'unique(ma_du_an)', 'Mã dự án phải là duy nhất!')
    ]

class CongViecDuAn(models.Model):
    _name = 'cong_viec_du_an'
    _description = 'Công việc trong dự án'
    _rec_name = 'ten_cong_viec'

    du_an_id = fields.Many2one('du_an', string="Dự án", ondelete='cascade', required=True)
    ten_cong_viec = fields.Char("Tên công việc", required=True)
    mo_ta = fields.Text("Chi tiết công việc")
    
    # Người thực hiện được chọn trực tiếp từ bảng nhân viên gốc
    nguoi_thuc_hien_id = fields.Many2one('nhan_vien', string="Người thực hiện", required=True)
    ngay_han = fields.Date("Hạn hoàn thành")
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_lam', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy bỏ')
    ], string="Trạng thái", default='moi', required=True)
