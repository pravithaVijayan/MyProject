# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ProductView(models.Model):
    # _name = "product.view"
    _inherit = 'product.template'
    product_master_type = fields.Selection([
        ('single', 'Single Product'),
        ('branded', 'Branded Products'),
    ], required=True, default='single')
    brand = fields.Many2one('product.brand', string='Brand')


class SalesProductView(models.Model):
    # _name = "product.view"
    _inherit = 'sale.order.line'
    brand = fields.Many2one('product.brand', string='Brand', related='product_id.brand')


class OrderView(models.Model):
    _inherit = 'res.partner'

    prime = fields.Boolean('Is a Prime member ')


class SalesOrderView(models.Model):
    _inherit = 'sale.order'

    is_prime = fields.Boolean('Is a Prime member ', related='partner_id.prime')
    brand = fields.Many2one('product.brand', string='Brand')



# class OrderView(models.Model):
#     # _name = "product.view"
#     _inherit = 'sale.order'
#
#     brand = fields.Many2one('product.brand', string='Brand', related='')


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    name = fields.Char(string='Name', required=True)

