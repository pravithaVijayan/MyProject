# -*- coding: utf-8 -*-


from odoo import api, fields, models, _, tools
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlrd
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class ImportReportWizard(models.TransientModel):
    _name = "import.report.wizard"

    book_id = fields.Many2one('product.product',
                              domain="[('product_tmpl_id.is_book', '=', True)]")

    def action_import_report(self):
        data = {
            'model': 'import.report.wizard',
            'form': self.read()[0]
        }
        print(data)
        return self.env.ref(
            'research_management.reservation_pdf').report_action(self,
                                                                 data=data)
