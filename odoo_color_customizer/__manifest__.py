# -*- coding: utf-8 -*-
{
    'name': 'Color Customizer',
    'version': '18.0.1.0.4',
    'category': 'Customizations',
    'summary': 'Customize Odoo primary brand color',
    'description': """
Color Customizer
================
Allow system administrators to change the primary brand color used throughout
the Odoo interface. Changes apply in real-time without page reload.

Features:
- Color picker in General Settings
- Live preview of color changes
- Persistent color setting across sessions
- Reset to default option
    """,
    'author': 'Odoo Color Customizer',
    'website': '',
    'depends': ['base_setup', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_color_customizer/static/src/scss/color_overrides.scss',
            'odoo_color_customizer/static/src/js/color_customizer.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
