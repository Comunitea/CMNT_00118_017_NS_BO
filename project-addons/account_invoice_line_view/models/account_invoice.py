# -*- coding: utf-8 -*-
#    Odoo, Open Source Management Solution
#    Copyright (C) 2014 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
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

from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    _order = 'id desc'

    @api.model_cr
    def init(self):
        # to be executed only when installing the module.update "stored" fields
        self._cr.execute("update account_invoice_line line \
                    set state = inv.state, date_invoice = inv.date_invoice, \
                    partner_id = inv.partner_id \
                    from account_invoice inv \
                    where line.invoice_id = inv.id")

    @api.multi
    def _get_base_amt(self):
        for invoice_line in self:
            curr_amt = invoice_line.price_subtotal
            # set the rate 1.0 if the transaction currency is the same as the
            # base currency
            if invoice_line.company_id.currency_id == invoice_line.currency_id:
                rate = 1.0
            else:
                if invoice_line.invoice_id.cc_amount_untaxed > 0:
                    rate = invoice_line.invoice_id.amount_untaxed / \
                        invoice_line.invoice_id.cc_amount_untaxed

            invoice_line.rate = rate
            invoice_line.base_amt = curr_amt / rate

    user_id = fields.Many2one('res.users', string="Comercial",
                              related='invoice_id.user_id')
    number = fields.Char(string='N factura', related='invoice_id.nmumber')
    # TODO no será selection mejor??
    state = fields.Selection(string="Estado", related='invoice_id.state',
                             store=True)
    date_invoice = fields.Date(string='Fecha Factura',
                               related='invoice_id.date_invoice', store=True)

    period_id = fields.Many2one('account.period', string="Periodo",
                                related='invoice_id.period_id')
    number = fields.Char(string='N factura', related='invoice_id.number')
    reference = fields.Char(string="Ref", related='invoice_id.reference')
    date_due = fields.Date(string='Fecha vto',
                           related='invoice_id.date_due')
    period_id = fields.Many2one('res.currency', string="Moneda",
                                related='invoice_id.currency_id')
    rate = fields.Float(string="Rate", compute='_get_base_amt')
    base_amt = fields.Float(string="Base Imponible", compute='_get_base_amt',
                            digits_compute=dp.get_precision('Account'))
    partner_id = fields.Many2one('res.partner', string="Cliente",
                                 related='invoice_id.partner_id', sotre=True)
