# -*- coding: utf-8 -*-
{
    'name': 'Quản lý Chấm công & Tính lương',
    'version': '1.0',
    'category': 'Human Resources',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_luong_co_ban_views.xml',
        'views/hr_cham_cong_views.xml',
        'views/hr_khen_thuong_ky_luat_views.xml',
        'views/hr_phieu_luong_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
