# -*- coding: utf-8 -*-
{
    'name': "quan_ly_van_ban",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "FIT-DNU",
    'website': "https://ttdn1501.aiotlabdnu.xyz/web",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'nhan_su', 'quan_ly_khach_hang'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/van_ban_den.xml',
        'views/van_ban_di.xml',
        'views/loai_van_ban.xml',
        'views/res_config_settings_views.xml',
        'views/khach_hang_views_inherit.xml',
        'views/menu.xml',
    ],
    # assets definitions
    'assets': {
        'web.assets_qweb': [
            'quan_ly_van_ban/static/src/xml/chat_widget.xml',
        ],
        'web.assets_backend': [
            'quan_ly_van_ban/static/src/css/chat_widget.css',
            'quan_ly_van_ban/static/src/js/chat_widget.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
