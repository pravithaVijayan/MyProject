# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        record_to_search = self.env['book.reservation'].search(
            [('name', '=', self.ref),
             ])
        if record_to_search:
            # print("hello")
            record_to_search.state = 'post'
        return super(AccountMove, self).action_post()


class SmartButtonContact(models.Model):
    _inherit = 'res.partner'
    responsible_user = fields.Char()

    def get_user(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'User',
            'view_mode': 'tree',
            'res_model': 'research.scholars',
            'domain': [('responsible_user', '=', self.name)],
            'context': "{'create': False}"
        }


class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean('Is a Book')


class BookReservation(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "book.reservation"

    # name = fields.Char(string="name")
    name = fields.Char(string='Scholar ID', readonly=True, required=True,
                       index=True, copy=False, default='New')
    scholars = fields.Many2one('research.scholars', string='Scholar')
    books = fields.Many2many('product.product',
                             domain="[('product_tmpl_id.is_book', '=', True)]")
    # books = fields.Many2many('product.product', 'reservation_id',
    #                         string='books',
    #                         domain="[('product_tmpl_id.is_book', '=', True)]",
    #                          )
    id = fields.Many2many(related='books.product_id')
    responsible_user = fields.Many2one('res.users', string='Responsible',
                                       default=lambda self: self.env.user.id)
    partner = fields.Many2one('res.partner', string="Related Partner",
                              related='scholars.contacts')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('cancel', 'Rejected')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False,
        default='draft', required=True, help='Book Reservation Request State')

    _sql_constraints = [
        ('reference_no_unique', 'unique(name)',
         'A Reference Number Must Be Unique!This Number Is Already Taken ,Please Try Another Number')]

    def action_confirm(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'

    def action_reject(self):
        self.state = 'cancel'

    @api.model
    def _compute_line_data_for_book_change(self, line):
        return {
            'name': line.name,
            'price_unit': line.lst_price,
            'product_id': line.id,
        }

    def data_line(self):
        order_lines = [(5, 0, 0)]
        for line in self.books:
            data = self._compute_line_data_for_book_change(line)
            order_lines.append((0, 0, data))
        return order_lines

    def action_create_invoice(self):
        # self.state = 'post'
        data = self.data_line()
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            # 'journal_id': 'Book',
            'ref': self.name,
            'state': 'draft',
            'partner_id': self.partner,
            'invoice_date': datetime.today(),
            'date': datetime.today(),
            'invoice_line_ids': data
        })

        # invoice.action_post()

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'book.reservation')
        return super(BookReservation, self).create(vals)


# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#
#     reservation_id = fields.Many2one('book.reservation')
