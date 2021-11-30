# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from  ast import literal_eval
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class BillofMaterialsProduct(models.TransientModel):
    _inherit = 'res.config.settings'

    is_product = fields.Boolean(string='Products',
                                config_parameter='website_bom_in_cart.is_product')
    product_ids = fields.Many2many('product.template', string="Products")

    # product_ids = fields.Integer(string="Products")
    def set_values(self):
        res = super(BillofMaterialsProduct, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'website_bom_in_cart.product_ids',
            self.product_ids.ids)
        # print(self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(BillofMaterialsProduct, self).get_values()
        # select_type = self.env['ir.config_parameter'].sudo()
        update_val = self.env['ir.config_parameter'].sudo().get_param(
            'website_bom_in_cart.product_ids')
        res.update({'product_ids': [(6, 0, literal_eval(update_val))]})
        # print(update_val)
        return res
