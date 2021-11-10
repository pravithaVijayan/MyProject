# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Material Request',
    'version': '14.0.1.0.0',
    'summary': '',
    'sequence': 10,
    'description': """ """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    'images': [],
    'depends': ['base_setup', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/cron.xml',
        'data/data1.xml',
        'wizard/import_lot_views.xml',
        'views/request.xml',
        'report/pdf_report.xml',
        'report/report_request_template.xml',
        # 'data/lot_and_series.xml',
        # 'views/lot_and_series.xml',

        # 'views/product.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_account_post_init',
    'license': 'LGPL-3',
}
