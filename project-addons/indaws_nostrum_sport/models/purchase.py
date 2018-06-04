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
from openerp import models, fields


class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    date_order = fields.Datetime(related='order_id.date_order',
                                 string="Fecha de pedido", readonly=True)
    ref_product = fields.Char(related='product_id.default_code',
                              string="Cod producto", readonly=True)
    partner_ref = fields.\
        Char(related='order_id.partner_id.property_account_payable_id.code',
             string="Num cuenta", readonly=True)
    customer_ref = fields.\
        Char(related='order_id.partner_id.property_account_payable_id.code',
             string="Num cliente", readonly=True)
    partner_vat = fields.Char(related='order_id.partner_id.vat',
                              string="NIF", readonly=True)
    partner_phone = fields.Char(related='order_id.partner_id.phone',
                                string="Tlf", readonly=True)
    partner_email = fields.Char(related='order_id.partner_id.email',
                                string="Email", readonly=True)
    partner_street = fields.Char(related='order_id.partner_id.street',
                                 string="Calle", readonly=True)
    partner_zip = fields.Char(related='order_id.partner_id.zip',
                              string="CP", readonly=True)
    partner_city = fields.Char(related='order_id.partner_id.city',
                               string="Ciudad", readonly=True)
    partner_state = fields.Char(related='order_id.partner_id.state_id.name',
                                string="Provincia", readonly=True)
