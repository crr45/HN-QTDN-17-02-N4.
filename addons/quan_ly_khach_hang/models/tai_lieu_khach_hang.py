# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TaiLieuKhachHang(models.Model):
    _name = 'tai_lieu_khach_hang'
    _description = 'Tài liệu/Hồ sơ khách hàng'
    _rec_name = 'ten_tai_lieu'

    khach_hang_id = fields.Many2one(
        'khach_hang', 
        string="Khách hàng", 
        required=True, 
        ondelete='cascade'
    )
    ten_tai_lieu = fields.Char("Tên tài liệu", required=True)
    loai_tai_lieu = fields.Selection([
        ('hop_dong', 'Hợp đồng'),
        ('bao_gia', 'Báo giá'),
        ('phap_ly', 'Tài liệu pháp lý'),
        ('khac', 'Tài liệu khác')
    ], string="Phân loại", required=True, default='khac')
    
    file_dinh_kem = fields.Binary("Tệp đính kèm")
    ten_file = fields.Char("Tên tệp")
    
    ngay_tai_len = fields.Date(
        "Ngày tải lên", 
        default=fields.Date.context_today
    )
    mo_ta = fields.Text("Mô tả chi tiết")
