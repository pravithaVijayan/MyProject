# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'pos.config'

    is_discount_limit = fields.Boolean(string="Discount Limit")
    discount_limit = fields.Integer(string='Limit',
                                    help="Limit used in the Point of Sale.")
    non_discount_categ_ids = fields.Many2many('pos.category', 'reference',
                                              string="discount")


class NonDiscountCategory(models.Model):
    _name = 'pos.category.nondiscount'

    categ_ids = fields.Many2many('pos.category', string="Categories")
    reference = fields.Many2one('pos.config')
