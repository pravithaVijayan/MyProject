# -*- coding: utf-8 -*-


from odoo import api, fields, models, _, tools
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlrd
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ImportReportWizard(models.TransientModel):
    _name = "import.report.wizard"

    book_ids = fields.Many2many('product.product',
                                domain="[('product_tmpl_id.is_book', '=', True)]",
                                required=True)
    scholar_id = fields.Many2one('research.scholars', string='Scholar',
                                 required=True)

    def action_report(self):
        domain = []
        domain_scholar = []
        scholar_id = self.scholar_id
        if scholar_id:
            domain_scholar += [('scholars', '=', scholar_id.id)]
        book_ids = []
        domain_names = []
        # domain_names = ['|']

        for book in self.book_ids:
            book_ids.append(book)
            domain_names.append(book.name)
        domain_books = []
        for book in book_ids:
            domain_books += ('books', '=', book.id),
        domain = []
        if domain_books:
            domain += (domain_books)
        if domain_scholar:
            domain += (domain_scholar)
        reservations = self.env['book.reservation'].search_read(domain)
        data = {
            # # 'model': 'import.report.wizard',
            'form': self.read()[0],
            'reservations': reservations,
            'book_ids': domain_names,
            # 'books': reservati
            'date':  date.today(),

        }
        print(data)
        return self.env.ref(
            'research_management.book_reservation_report_pdf_wizard').report_action(
            self, data=data)
