# -*- coding: utf-8 -*-
{
    'name': 'Quản lý Tài sản',
    'version': '1.0',
    'summary': 'Quản lý thông tin tài sản và bàn giao tài sản dựa trên dữ liệu nhân sự gốc.',
    'category': 'Asset',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/tai_san_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
