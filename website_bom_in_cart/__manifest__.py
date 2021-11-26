# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website - BOM in Cart',
    'version': '14.0.1.0.0',
    'summary': 'Website Management Software',
    'sequence': 10,
    'description': """ Website management software """,
    'category': 'Website/eLearning',
    'website': 'https://www.odoo.com/page/billing',
    'images': [],
    'depends': ['base_setup', 'mrp'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/website_config_settings.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_account_post_init',
    # 'license': 'LGPL-3',
}
