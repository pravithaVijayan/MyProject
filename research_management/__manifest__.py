# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Research Management',
    'version' : '14.0.1.0.0',
    'summary': 'Research Management Software',
    'sequence': 10,
    'description': """ Research management software """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base_setup','contacts','sale_management','mail','product','account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/research.xml',
        'views/book_reservation.xml',
        'data/data.xml',
        'data/data2.xml'
        # 'views/sales_book.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_account_post_init',
    'license': 'LGPL-3',
}