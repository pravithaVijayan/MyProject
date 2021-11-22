# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'POS Product Discription',
    'version': '14.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'sequence': 3,
    'summary': 'Product Description in the Point of Sale ',
    'description': """""",
    'depends': ['point_of_sale'],
    'data': [
        'views/product_view.xml',
        'views/point_of_sale.xml',
    ],
    'qweb': [
        'static/src/xml/pos_order_line.xml',
        'static/src/xml/receipt.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
