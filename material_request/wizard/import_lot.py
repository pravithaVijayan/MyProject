# -*- coding: utf-8 -*-


from odoo import api, fields, models, _, tools
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlrd
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ImportLotsWizard(models.TransientModel):
    _name = "import.lots.wizard"

    file_name = fields.Char(string="Enter File Path", required=True)

    def action_import_lots(self):
        loc = self.file_name
        wb = xlrd.open_workbook(loc)
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
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Datas Successfully Imported',
                'type': 'rainbow_man',
            }
        }
    # try:
    #     book = xlrd.open_workbook(filename=self.file_name)
    # except FileNotFoundError:
    #     raise UserError(
    #         'No such file or directory found. \n%s.' % self.file_name)
    # except xlrd.biffh.XLRDError:
    #     raise UserError('Only excel files are supported.')
    # for sheet in book.sheets():
    #     try:
    #         if sheet.name == 'Sheet1':
    #             for row in range(sheet.nrows):
    #                 if row >= 1:
    #                     row_values = sheet.row_values(row)
    #                     lot = self.env['stock.production.lot'].create({
    #                         'name': row_values[1],
    #                         'product_id': row_values[2],
    #                         'company_id': row_values[4],
    #                     })
    # vals = self._create_lots_entry(row_values)
    # line_vals.append((0, 0, vals))
    # if line_vals:
    #     date = self.date
    #     ref = self.jv_ref
    #     self.env['account.move'].create({
    #         'date': date,
    #         'ref': ref,
    #         'journal_id': self.jv_journal_id.id,
    #         'line_ids': line_vals
    #     })
    # except IndexError:
    #     pass
