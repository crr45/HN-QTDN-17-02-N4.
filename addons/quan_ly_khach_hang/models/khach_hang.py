# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Thông tin khách hàng'
    _rec_name = 'ten_khach_hang'

    ma_khach_hang = fields.Char("Mã khách hàng", required=True)
    ten_khach_hang = fields.Char("Họ và tên khách hàng", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string="Giới tính", default='nam')
    so_dien_thoai = fields.Char("Số điện thoại")
    email = fields.Char("Email")
    dia_chi = fields.Char("Địa chỉ")
    ma_so_thue = fields.Char("Mã số thuế")
    
    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách")
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('tiep_can', 'Tiếp cận'),
        ('tiem_nang', 'Tiềm năng'),
        ('hop_dong', 'Đã ký hợp đồng'),
        ('ngung_hop_tac', 'Ngừng hợp tác')
    ], string="Trạng thái", default='moi')
    
    mo_ta = fields.Text("Mô tả/Ghi chú")
    
    tai_lieu_ids = fields.One2many(
        'tai_lieu_khach_hang', 
        'khach_hang_id', 
        string="Hồ sơ đính kèm"
    )

    _sql_constraints = [
        ('ma_khach_hang_unique', 'unique(ma_khach_hang)', 'Mã khách hàng phải là duy nhất!')
    ]
