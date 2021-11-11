# -*- coding: utf-8 -*-
from odoo import models


class MaterialRequestXlsx(models.AbstractModel):
    _name = 'report.material_request.report_request_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, requsts):
        sheet = workbook.add_worksheet('Material Requests')
        bold = workbook.add_format({'bold': True})
        row = 0
        col = 0
        for obj in requsts:
            sheet.write(row, col, obj.name, bold)
            row += 1
