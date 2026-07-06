# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HRPhieuLuong(models.Model):
    _name = 'hr_phieu_luong'
    _description = 'Phiếu lương tháng nhân viên'
    _rec_name = 'display_name'

    thang = fields.Integer("Tháng", required=True, default=lambda self: fields.Date.today().month)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)

    so_ngay_di_lam = fields.Float("Số ngày đi làm thực tế", compute="_compute_so_ngay_di_lam")
    luong_co_ban = fields.Float("Lương cơ bản (VND)", compute="_compute_luong_info")
    phu_cap_an_trua = fields.Float("Phụ cấp ăn trưa", compute="_compute_luong_info")
    phu_cap_trach_nhiem = fields.Float("Phụ cấp trách nhiệm", compute="_compute_luong_info")
    khen_thuong = fields.Float("Khen thưởng", compute="_compute_khen_thuong_ky_luat")
    ky_luat = fields.Float("Kỷ luật", compute="_compute_khen_thuong_ky_luat")
    thuc_linh = fields.Float("Thực lĩnh", compute="_compute_thuc_linh")
    
    display_name = fields.Char("Tên phiếu lương", compute="_compute_display_name")

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_display_name(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                record.display_name = f"Phiếu lương - {record.nhan_vien_id.ho_va_ten} - {record.thang}/{record.nam}"
            else:
                record.display_name = "Phiếu lương"

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_ngay_di_lam(self):
        for record in self:
            if not record.nhan_vien_id or not record.thang or not record.nam:
                record.so_ngay_di_lam = 0.0
                continue
            attendances = self.env['hr_cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id)
            ])
            total_days = 0.0
            for att in attendances:
                if att.ngay_cham_cong and att.ngay_cham_cong.month == record.thang and att.ngay_cham_cong.year == record.nam:
                    if att.trang_thai == 'di_lam':
                        total_days += 1.0
                    elif att.trang_thai == 'nua_ngay':
                        total_days += 0.5
            record.so_ngay_di_lam = total_days

    @api.depends('nhan_vien_id')
    def _compute_luong_info(self):
        for record in self:
            if not record.nhan_vien_id:
                record.luong_co_ban = 0.0
                record.phu_cap_an_trua = 0.0
                record.phu_cap_trach_nhiem = 0.0
                continue
            luong_cfg = self.env['hr_luong_co_ban'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id)
            ], limit=1)
            if luong_cfg:
                record.luong_co_ban = luong_cfg.luong_co_ban
                record.phu_cap_an_trua = luong_cfg.phu_cap_an_trua
                record.phu_cap_trach_nhiem = luong_cfg.phu_cap_trach_nhiem
            else:
                record.luong_co_ban = 0.0
                record.phu_cap_an_trua = 0.0
                record.phu_cap_trach_nhiem = 0.0

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_khen_thuong_ky_luat(self):
        for record in self:
            if not record.nhan_vien_id or not record.thang or not record.nam:
                record.khen_thuong = 0.0
                record.ky_luat = 0.0
                continue
            kt_kl_records = self.env['hr_khen_thuong_ky_luat'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id)
            ])
            total_thuong = 0.0
            total_phat = 0.0
            for item in kt_kl_records:
                if item.ngay_ap_dung and item.ngay_ap_dung.month == record.thang and item.ngay_ap_dung.year == record.nam:
                    if item.loai_quyet_dinh == 'thuong':
                        total_thuong += item.so_tien
                    elif item.loai_quyet_dinh == 'phat':
                        total_phat += item.so_tien
            record.khen_thuong = total_thuong
            record.ky_luat = total_phat

    @api.depends('luong_co_ban', 'so_ngay_di_lam', 'phu_cap_an_trua', 'phu_cap_trach_nhiem', 'khen_thuong', 'ky_luat')
    def _compute_thuc_linh(self):
        for record in self:
            phu_cap = record.phu_cap_an_trua + record.phu_cap_trach_nhiem
            record.thuc_linh = (record.luong_co_ban / 26.0) * record.so_ngay_di_lam + phu_cap + record.khen_thuong - record.ky_luat
