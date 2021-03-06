# -*- coding: utf-8 -*-


from odoo import api, fields, models, _, tools
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlrd
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ImportReportWizard(models.TransientModel):
    _name = "report.wizard"

    book_ids = fields.Many2many('product.product',
                                domain="[('product_tmpl_id.is_book', '=', True)]",
                                )
    scholar_id = fields.Many2one('research.scholars', string='Scholar',
                                 )

    def action_xlsx_report(self):
        domain = []
        domain_scholar = []
        scholar_id = self.scholar_id
        if scholar_id:
            domain_scholar += [('scholars', '=', scholar_id.id)]
        book_ids = []
        domain_names = []
        for book in self.book_ids:
            book_ids.append(book)
            domain_names.append(book.name)
        domain_books = []
        for book in book_ids:
            domain_books += ('books', '=', book.id),
        if domain_books:
            domain += (domain_books)
        if domain_scholar:
            domain += (domain_scholar)
        if len(domain) > 0:
            reservations = self.env['book.reservation'].search_read(domain)
        else:
            reservations = self.env['book.reservation'].search_read()
        data = {
            'form': self.read()[0],
            'reservations': reservations,
            'book_ids': domain_names,
            'date': date.today(),
        }
        return self.env.ref(
            'research_management.action_report_xlsx').report_action(
            self, data=data)

    def action_report(self):
        domain_names = []
        for book in self.book_ids:
            domain_names.append(book.name)
        if self.scholar_id and self.book_ids:
            data = {
                'scholars_id': self.scholar_id.id,
                'state': 'cancel',
                'books': tuple(domain_names),
            }
            self.env.cr.execute("""
                                          SELECT 
                                                  b.name as name,
                                                  b.state as state,
                                                  r.name as responsible_user
                      FROM 
                          book_reservation b
                          LEFT OUTER JOIN res_partner r ON(b.responsible_user+1=r.id)
                          LEFT OUTER JOIN product_book p ON(b.id=p.reservation_id)
                    WHERE (b.scholars =%(scholars_id)s AND b.state <> %(state)s ) AND 
                            p.product_name IN %(books)s
                                  """, data)
        elif self.scholar_id:
            data = {
                'scholars_id': self.scholar_id.id,
                'state': 'cancel',
            }
            self.env.cr.execute("""
                                          SELECT 
                                                  b.name as name,
                                                  b.state as state,
                                                  r.name as responsible_user
                      FROM 
                          book_reservation b
                          LEFT OUTER JOIN res_partner r ON(b.responsible_user+1=r.id)
                    WHERE (b.scholars =%(scholars_id)s AND b.state <> %(state)s )
                                  """, data)
        else:
            self.env.cr.execute("""SELECT 
                                                  b.name as name,
                                                  b.state as state,
                                                  r.name as responsible_user
                      FROM 
                          book_reservation b
                          LEFT OUTER JOIN res_partner r ON(b.responsible_user+1=r.id)
                                """)
        result = self.env.cr.dictfetchall()
        # print(result)
        data = {
            'form': self.read()[0],
            'reservations': result,
            'book_ids': domain_names,
            'date': date.today(),
        }
        return self.env.ref(
            'research_management.book_reservation_report_pdf_wizard').report_action(
            self, data=data)
