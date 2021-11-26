# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class DiscountLimit(models.TransientModel):
    _inherit = 'res.config.settings'

    is_product = fields.Boolean(string='Products')
    product_ids = fields.Many2many('product.template', string="Products")


