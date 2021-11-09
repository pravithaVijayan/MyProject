# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
import os
import xlrd

from odoo.osv import osv


class SalesProductView(models.Model):
    _inherit = 'stock.production.lot'

    def import_record(self):
        loc = ('/home/ubuntu/Downloads/import2.xlsx')
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        # print(sheet.ncols)
        sheet = wb.sheet_by_index(0)
        # print(sheet.ncols)
        for cols in range(1, sheet.ncols + 1):
            product = self.env['product.product'].search(
                [('name', '=', sheet.cell_value(cols, 1))])
            company = self.env['res.company'].search(
                [('name', '=', sheet.cell_value(cols, 2))])
            # print(product, company)
            self.env['stock.production.lot'].create({
                'name': sheet.cell_value(cols, 0),
                'product_id': product.id,
                'company_id': company.id,
            })


class ProductBrand(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "product.request"
    _description = "Product request"

    name = fields.Char(string='Request ID', readonly=True, required=True,
                       index=True, copy=False, default='New')
    responsible_user = fields.Many2one('res.users', string='Responsible',
                                       default=lambda self: self.env.user.id)
    product_ids = fields.One2many('product.line', 'product_request_id',
                                  string="Products")
    approval_count = fields.Integer(default=0)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'First Approval'),
        ('second_approve', 'second Approval'),
        ('approved', 'Approved'),
        ('cancel', 'Rejected')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False,
        default='draft', required=True, help='Material Request State')

    def action_confirm(self):
        self.state = 'submit'

    def action_approve(self):
        search_data = self.env['product.request'].search(
            [('name', '=', self.name)])
        count = search_data.approval_count
        if count == 0:
            self.state = 'second_approve'
            search_data.approval_count = 1
        if count == 1:
            self.state = 'approved'
            search_data.approval_count = 2
            for line in search_data.product_ids:
                if line.route == 'mto':
                    self.create_rfq(line)

    @api.model
    def _compute_line_data(self, line):
        return {
            'product_id': line.product_id.id,
            'name': line.product_id.name,
            'product_qty': line.product_uom_qty,
            'price_unit': line.price_unit,
        }

    def data_line(self):
        order_lines = [(5, 0, 0)]
        for line in self.product_ids:
            if line.route == 'mto':
                data = self._compute_line_data(line)
                order_lines.append((0, 0, data))
        return order_lines

    def create_rfq(self, line):
        for vendor in line.product_tmpl_id.seller_ids:
            if vendor:
                data = self.data_line()
                rfq = self.env['purchase.order'].create({
                    'partner_id': vendor.name.id,
                    'state': 'draft',
                    'order_line': data,
                })

    def action_reject(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'product.request')
        return super(ProductBrand, self).create(vals)


class ProductOrderLine(models.Model):
    _name = 'product.line'
    # _order = 'product_id'
    product_request_id = fields.Many2one('product.request')
    product_id = fields.Many2one('product.product', string='Product Lines',
                                 required=True)
    price_unit = fields.Float('Unit Price', related="product_id.list_price",
                              required=True,
                              digits='Product Price', default=0.0)
    product_tmpl_id = fields.Many2one(related='product_id.product_tmpl_id')
    route = fields.Selection([
        ('internal', 'Internal'),
        ('mto', 'MTO')
    ], index=True, default='internal')
    product_uom_qty = fields.Float(string='Quantity',
                                   digits='Product Unit of Measure',
                                   required=True, default=1.0)
