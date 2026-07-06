# -*- coding: utf-8 -*-
from odoo import models, fields

class KhachHang(models.Model):
    _inherit = 'khach_hang'

    van_ban_den_ids = fields.One2many(
        'van_ban_den', 
        'khach_hang_id', 
        string="Văn bản đến liên quan"
    )
    van_ban_di_ids = fields.One2many(
        'van_ban_di', 
        'khach_hang_id', 
        string="Văn bản đi liên quan"
    )
