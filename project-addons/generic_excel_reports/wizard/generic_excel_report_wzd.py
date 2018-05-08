# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 BrowseInfo(<http://www.browseinfo.in>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
import xlwt
import cStringIO
import base64


class GenericExcelReportWizard(models.TransientModel):
    _name = "generic.excel.report.wizard"

    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)

    @api.multi
    def print_report(self):
        stylePC = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        fontP = xlwt.Font()
        fontP.bold = True
        stylePC.font = fontP
        stylePC.num_format_str = '@'
        stylePC.alignment = alignment
        style_n = xlwt.easyxf("font:height 300; font: name Liberation Sans, \
            bold on,color black; align: horiz center")
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Generic Excel Report")
        cur = self._context["active_model"]
        globle_obj = self.env['generic.excel.report']
        curr_obj = self.env[cur]
        field_dict = {}
        field_dict_name = {}
        field_dict_sequence = {}
        globle_id = self._context.get('globle')
        id = self._context.get('active_ids')
        f = globle_obj.browse(globle_id).field_ids
        worksheet.write_merge(0, 1, 0, (len(f) - 1),
                              globle_obj.browse(globle_id).name, style=style_n)
        for dummy_field in sorted(f, key=lambda x: x.sequence_excel):
            field_dict[dummy_field.field_id.name] = dummy_field.field_id.ttype
            field_dict_name[dummy_field.field_id.name] = \
                dummy_field.field_id.field_description
            field_dict_sequence[dummy_field.field_id.name] = \
                dummy_field.sequence_excel
        row = 0
        col = 3
        for i in id:
            if row == 0 and col == 3:
                for dummy_field in sorted(field_dict_sequence,
                                          key=field_dict_sequence.get):
                    worksheet.write(col, row, field_dict_name[dummy_field],
                                    style=stylePC)
                    row = row + 1
            col = col + 1
            row = 0
            for dummy_field1 in sorted(field_dict_sequence,
                                       key=field_dict_sequence.get):
                record = getattr(curr_obj.browse(i), dummy_field1)
                if field_dict[dummy_field1] == "many2one":
                    record = record.name
                worksheet.write(col, row, record)
                row = row + 1
            # col=col+1

        file_data = cStringIO.StringIO()
        workbook.save(file_data)
        self.write({
            'state': 'get',
            'data': base64.encodestring(file_data.getvalue()),
            'name': "informe-excel.xls"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generic Excel Report',
            'res_model': 'generic.excel.report.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }
