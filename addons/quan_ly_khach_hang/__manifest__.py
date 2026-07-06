# -*- coding: utf-8 -*-
{
    'name': "quan_ly_khach_hang",
    'summary': """
        Quản lý thông tin khách hàng và số hóa tài liệu hồ sơ đính kèm.""",
    'description': """
        Mô-đun quản lý khách hàng cho Odoo 15:
        - Quản lý thông tin chi tiết khách hàng.
        - Gán nhân viên phụ trách từ mô-đun nhân sự.
        - Số hóa và đính kèm trực tiếp hợp đồng, báo giá, tài liệu pháp lý.
    """,
    'author': "FIT-DNU",
    'website': "https://ttdn1501.aiotlabdnu.xyz/web",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/khach_hang_views.xml',
        'views/menu.xml',
    ],
    'application': True,
}
