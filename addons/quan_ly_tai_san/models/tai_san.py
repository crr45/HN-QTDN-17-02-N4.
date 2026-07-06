# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Thông tin tài sản'
    _rec_name = 'ten_tai_san'

    ma_tai_san = fields.Char("Mã tài sản", required=True)
    ten_tai_san = fields.Char("Tên tài sản", required=True)
    loai_tai_san = fields.Selection([
        ('thiet_bi', 'Thiết bị công nghệ (Laptop, PC...)'),
        ('van_phong', 'Đồ văn phòng (Bàn, ghế...)'),
        ('phuong_tien', 'Phương tiện đi lại'),
        ('khac', 'Tài sản khác')
    ], string="Loại tài sản", default='thiet_bi', required=True)
    gia_tri = fields.Float("Giá trị tài sản (VND)", default=0.0)
    ngay_mua = fields.Date("Ngày mua")
    ghi_chu = fields.Text("Ghi chú")
    
    # Bàn giao tài sản liên kết với nhân sự và đơn vị gốc từ phân hệ nhan_su
    nguoi_su_dung_id = fields.Many2one('nhan_vien', string="Người sử dụng")
    don_vi_quan_ly_id = fields.Many2one('don_vi', string="Đơn vị quản lý")
    
    trang_thai = fields.Selection([
        ('trong_kho', 'Trong kho / Chưa bàn giao'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('hong_hoc', 'Đang hỏng hóc/Sửa chữa'),
        ('thanh_ly', 'Đã thanh lý')
    ], string="Trạng thái", default='trong_kho', required=True)

    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải là duy nhất!')
    ]
