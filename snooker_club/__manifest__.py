# -*- coding: utf-8 -*-
{
    'name': "Snooker Club",

    'summary': """
        Snooker Club gets data via api, manage player records and events.""",

    'description': """
        Odoo is a fully integrated suite of business modules that encompass the traditional ERP functionality.
        
    """,

    'author': "Niaz Ahmed Raza",
    'website': "",

    'category': 'Sale',
    'version': '0.1',
    'depends': ['base', 'sale_management'],
    'images': [
        'static/description/banner.png',
        'static/description/banner1.gif',
    ],
    'price': 0,
    'currency': 'EUR',
    "license": "OPL-1",
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/message_wizard.xml',
        'data/schedulers.xml',
    ],
}
