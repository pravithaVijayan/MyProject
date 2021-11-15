# -*- coding: utf-8 -*-
from odoo import models


class BookReservationXlsx(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.research_management.report_books_xls'

    def generate_xlsx_report(self, workbook, data, requsts):
        sheet = workbook.add_worksheet('Reservations')
        bold = workbook.add_format({'bold': True})
        bold_light = workbook.add_format({'bold': True,'bg_color': '#C0C0C0'})
        bold_dark = workbook.add_format({'bold': True,'bg_color': '#808080'})
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 15)
        sheet.merge_range('D1:F1', 'BOOK RESERVATION REPORT', bold_light)
        row = 2
        col = 1
        sheet.write(1, 1, 'Scholar', bold)
        if data['form']['scholar_id']:
            sheet.write(1, 2, data['form']['scholar_id'][1])
        sheet.write(2, 1, 'books', bold)
        if data['book_ids']:
            for book in data['book_ids']:
                sheet.write(row, col + 1, book)
                row += 1
        else:
            row += 1
        sheet.write(row, 1, 'Date', bold)
        sheet.write(row, 2, data['date'])
        row = 5
        col = 3
        sheet.write(row, col, 'Reference', bold_dark)
        sheet.write(row, col + 1, 'Responsible', bold_dark)

        for obj in data['reservations']:
            row += 1
            sheet.write(row, col, obj['name'])
            sheet.write(row, col + 1, obj['responsible_user'][1])
