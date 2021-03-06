# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'POS Product Discount',
    'version': '14.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'sequence': 1,
    'summary': 'Product Description in the Point of Sale ',
    'description': """""",
    'depends': ['point_of_sale','pos_discount'],
    'data': [
        'views/pos_config_discount.xml',
        'views/point_of_sale_template.xml',
    ],
    'qweb': [
        # 'static/src/xml/pos_order_line.xml',
        # 'static/src/xml/receipt.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
