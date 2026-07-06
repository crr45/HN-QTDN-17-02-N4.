# -*- coding: utf-8 -*-
{
    'name': 'Quản lý Dự án',
    'version': '1.0',
    'summary': 'Quản lý thông tin dự án và phân công công việc dựa trên nhân sự gốc.',
    'category': 'Project',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/du_an_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
