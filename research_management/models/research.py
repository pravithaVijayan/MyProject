# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SalesBookOrderView(models.Model):
    _inherit = 'sale.order'

    book_reservation = fields.Many2one('book.reservation',
                                       string='Book Reservation')

    @api.model
    def _compute_line_data_for_book_change(self, line):
        return {

            'name': line.name,
            'price_unit': line.lst_price,
            'product_id': line.id,
        }

    @api.onchange('book_reservation')
    def onchange_sale_order_book_id(self):
        template = self.book_reservation.with_context(
            lang=self.partner_id.lang)

        self.partner_id = template.partner

        # --- first, process the list of products from the template
        order_lines = [(5, 0, 0)]
        for line in template.books:
            data = self._compute_line_data_for_book_change(line)
            order_lines.append((0, 0, data))

        self.order_line = order_lines


class ResearchScholars(models.Model):
    _inherit = 'res.partner'

    is_scholar = fields.Boolean('Is a Scholar ')


class ResearchScholar(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "research.scholars"
    _description = "Research Scholars"

    name = fields.Char(compute='comp_name', string='Scholar Name', store=True)
    scholar_id = fields.Char(string='Scholar ID', readonly=True, required=True,
                             index=True, copy=False, default='New')
    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name', required=True)
    age = fields.Integer(string='Age')
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    institute = fields.Many2one('institute.details', string='Institute Name',
                                tracking=True, required=True)
    address = fields.Text(string='Address', related='institute.address')
    phone = fields.Char(string='Contact Number', related='institute.phone')
    note = fields.Text(string=' Add Additional Note')
    contacts = fields.Many2one('res.partner',
                               domain="[('is_scholar','=','True')]")
    responsible_user = fields.Char(string="Related Partner",
                                   related='contacts.name')

    @api.model
    def create(self, vals):
        vals['scholar_id'] = self.env['ir.sequence'].next_by_code(
            'research.scholars')
        return super(ResearchScholar, self).create(vals)

    @api.depends('first_name', 'middle_name', 'last_name')
    def comp_name(self):
        self.name = (self.first_name or '') + ' ' + (self.middle_name or '') \
                    + ' ' + (self.last_name or '')

    _sql_constraints = [
        ('scholar_id_unique', 'unique(scholar_id)',
         'A Scholar ID Must Be Unique!This Number Is Already Taken ,Please Try Another Number')]

    class Institute(models.Model):
        _name = "institute.details"

        name = fields.Char(string='Institute Name', required=True)
        address = fields.Text(string='Address')
        phone = fields.Char(string='Contact Number')
