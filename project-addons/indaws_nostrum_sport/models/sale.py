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


class SaleOrderLine(models.Model):
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
    margin_ptje_min = fields.Float(digits=(6, 2), string="Margen Min (%)",
                               compute='_get_margin_ptje')
    margin_euros_min = fields.Float(digits=(6, 2), string="Margen Min",
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
    price_min = fields.Float(digits=(6, 2), string="Precio mínimo")

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        """
        Añado el cálculo del precio mínimo vasado en tarifa
        """
        res = super(SaleOrderLine, self).product_id_change()
        if not self.product_id:
            return res
        min_price_pl = self.env.ref('indaws_nostrum_sport.pricelist_min_price')
        price_min = min_price_pl.get_product_price(
            self.product_id, self.product_uom_qty or 1.0, 
            self.order_id.partner_id)
        self.price_min = price_min
        return res

    @api.model
    def _get_margin_ptje(self):
        """
        Calculo el margen basado en precio mínimo
        """
        for record in self:
            record.margin_euros = record.price_subtotal - \
                record.purchase_price * record.product_uom_qty
            record.margin_euros_min = record.price_subtotal - \
                record.price_min * record.product_uom_qty
            margen = 0
            margen_min = 0
            if record.price_subtotal != 0.0:
                margen = (record.margin_euros / record.price_subtotal) * 100
                margen_min = (record.margin_euros_min / record.price_subtotal) * 100
            record.margin_ptje = margen
            record.margin_ptje_min = margen_min
    
    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Propago min price a la factura
        """
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update(price_min=self.price_min)
        return res

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
    margin_euros_min = fields.Float(digits=(6, 2), string="Margen Min",
                                    compute='_get_margin_ptje')
    margin_ptje_min = fields.Float(digits=(6, 2), string="Margen Min (%)",
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
            margin_euros_min = 0.0
            for elem in record.order_line:
                margin_euros = margin_euros + elem.margin_euros
                margin_euros_min += elem.margin_euros_min
            margen = 0
            margen_min = 0
            if record.amount_untaxed != 0.0:
                margen = (margin_euros / record.amount_untaxed) * 100
                margen_min = (margin_euros_min / record.amount_untaxed) * 100
            
            record.margin_euros = margin_euros
            record.margin_ptje = margen
            record.margin_euros_min = margin_euros_min
            record.margin_ptje_min = margen_min
