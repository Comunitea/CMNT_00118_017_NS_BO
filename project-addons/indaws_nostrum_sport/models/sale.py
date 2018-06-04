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


class SAaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    date_order = fields.Datetime(related='order_id.date_order',
                                 string="Fecha de pedido", readonly=True)
    ref_product = fields.Char(related='product_id.default_code',
                              string="Cod producto", readonly=True)
    partner_email = fields.Char(related='order_partner_id.email',
                                string="Email", readonly=True)

    margin_ptje = fields.Float(digits=(6, 2), string="Margen (%)",
                               compute='_get_margin_ptje')
    margin_euros = fields.Float(digits=(6, 2), string="Margen",
                                compute='_get_margin_ptje')
    price_unit_net = fields.Float(digits=(6, 2), string="Precio neto unitario",
                                  compute='_get_net_unit')
    # MIGRATION el property_account_receivable_id se le añade_id
    customer_ref = fields.\
        Char(related='order_id.partner_id.customer_ref',
             string="Num cuenta", readonly=True)
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

    @api.model
    def _get_margin_ptje(self):
        for record in self:
            record.margin_euros = record.price_subtotal - \
                record.purchase_price * record.product_uom_qty
            margen = 0
            if record.price_subtotal != 0.0:
                margen = (record.margin_euros / record.price_subtotal) * 100
            record.margin_ptje = margen

    @api.model
    def _get_net_unit(self):
        for record in self:
            record.price_unit_net = record.price_unit - \
                record.price_unit * (record.discount / 100)


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    margin_euros = fields.Float(digits=(6, 2), string="Margen",
                                compute='_get_margin_ptje')
    margin_ptje = fields.Float(digits=(6, 2), string="Margen (%)",
                               compute='_get_margin_ptje')
    url_presupuesto = fields.Char(string="Url presupuesto")
    texto_presupuesto = fields.Char(string="Texto presupuesto")

    partner_zip = fields.Char(related='partner_id.zip',
                              string="CP", readonly=True)
    partner_city = fields.Char(related='partner_id.city',
                               string="Ciudad", readonly=True)
    partner_state = fields.Char(related='partner_id.state_id.name',
                                string="Provincia", readonly=True)

    def _get_margin_ptje(self):
        for record in self:
            margin_euros = 0.0
            for elem in record.order_line:
                margin_euros = margin_euros + elem.margin_euros
            margen = 0
            if record.amount_untaxed != 0.0:
                margen = (margin_euros / record.amount_untaxed) * 100
            record.margin_euros = margin_euros
            record.margin_ptje = margen
