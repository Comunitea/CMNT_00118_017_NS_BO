# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


from openerp import models, fields, api


class Saleorder(models.Model):

    _name = "sale.order"
    _inherit = "sale.order"

    base_21 = fields.Float(digits=(6, 2), string="Base 21%",
                           compute='_get_importe_impuestos',)
    iva_21 = fields.Float(digits=(6, 2), string="IVA 21%",
                          compute='_get_importe_impuestos',)
    base_10 = fields.Float(digits=(6, 2), string="Base 10%",
                           compute='_get_importe_impuestos',)
    iva_10 = fields.Float(digits=(6, 2), string="IVA 10%",
                          compute='_get_importe_impuestos',)
    base_4 = fields.Float(digits=(6, 2), string="Base 4%",
                          compute='_get_importe_impuestos',)
    iva_4 = fields.Float(digits=(6, 2), string="IVA 4%",
                         compute='_get_importe_impuestos',)
    base_0 = fields.Float(digits=(6, 2), string="Base 0%",
                          compute='_get_importe_impuestos',)
    iva_0 = fields.Float(digits=(6, 2), string="IVA 0%",
                         compute='_get_importe_impuestos',)

    base_req = fields.Float(digits=(6, 2), string="Base Req",
                            compute='_get_importe_impuestos',)
    ptje_req = fields.Float(digits=(6, 2), string="Porcentaje Req",
                            compute='_get_importe_impuestos',)
    cuota_req = fields.Float(digits=(6, 2), string="Cuota Req%",
                             compute='_get_importe_impuestos',)

    @api.depends('order_line')
    def _get_importe_impuestos(self):
        for record in self:

            base_21 = 0.0
            iva_21 = 0.0
            base_10 = 0.0
            iva_10 = 0.0
            base_4 = 0.0
            iva_4 = 0.0
            base_0 = 0.0
            iva_0 = 0.0

            base_req = 0.0
            ptje_req = 0.0
            cuota_req = 0.0

            for line in record.order_line:
                if line.tax_id:
                    for tax in line.tax_id:
                        if 'IVA' in tax.name:
                            if tax.amount >= 0.209 and tax.amount <= 0.211:
                                base_21 = base_21 + line.price_subtotal
                            if tax.amount >= 0.09 and tax.amount <= 0.11:
                                base_10 = base_10 + line.price_subtotal
                            if tax.amount >= 0.03 and tax.amount <= 0.05:
                                base_4 = base_4 + line.price_subtotal
                            if tax.amount == 0.00:
                                base_0 = base_0 + line.price_subtotal

                        if 'Recargo' in tax.name or \
                                'Recargo' in tax.description:
                            ptje_req = tax.amount
                            base_req = base_req + line.price_subtotal

            iva_21 = base_21 * 0.21
            iva_10 = base_10 * 0.10
            iva_4 = base_4 * 0.04

            cuota_req = ptje_req * base_req

            record.base_21 = base_21
            record.iva_21 = iva_21
            record.base_10 = base_10
            record.iva_10 = iva_10
            record.base_4 = base_4
            record.iva_4 = iva_4
            record.base_0 = base_0
            record.iva_0 = iva_0

            record.base_req = base_req
            record.ptje_req = ptje_req
            record.cuota_req = cuota_req
