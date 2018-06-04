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
from odoo import models, fields, api


class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit = 'pos.order'
    # MIGRATION el property_account_receivable_id se le añade_id
    partner_ref = fields.\
        Char(related='partner_id.property_account_receivable_id.code',
             string="Num cuenta", readonly=True)
    partner_ref = fields.\
        Char(related='partner_id.customer_ref',
             string="Num cliente", readonly=True)
    partner_vat = fields.Char(related='partner_id.vat', string="NIF",
                              readonly=True)
    partner_phone = fields.Char(related='partner_id.phone',
                                string="Tlf", readonly=True)
    partner_email = fields.Char(related='partner_id.email',
                                string="Email", readonly=True)
    invoice_date_due = fields.Date(related='invoice_id.date_due',
                                   string="Vencimiento", readonly=True)
    invoice_payment_mode = fields.\
        Char(related='invoice_id.payment_mode_id.name',
             string="Modo de pago", readonly=True)
    total_neto = fields.Float(digits=(6, 2), string="Total neto",
                              compute='_get_total_neto')
    partner_zip = fields.Char(related='partner_id.zip',
                              string="CP", readonly=True)
    partner_city = fields.Char(related='partner_id.city',
                               string="Ciudad", readonly=True)
    partner_state = fields.Char(related='partner_id.state_id.name',
                                string="Provincia", readonly=True)

    @api.multi
    def _get_total_neto(self):
        for record in self:
            record.total_neto = record.amount_total - record.amount_tax
