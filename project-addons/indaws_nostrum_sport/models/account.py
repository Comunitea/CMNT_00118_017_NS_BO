﻿# -*- coding: utf-8 -*-
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
from openerp import api, models, fields
from datetime import datetime


class AccountInvoiceLine(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    partner_ref = fields.Char(related='invoice_id.account_id.code',
                              string="Num cuenta", readonly=True)
    customer_ref = fields.Char(related='invoice_id.account_id.code',
                               string="Num cliente", readonly=True)
    partner_vat = fields.Char(related='invoice_id.partner_id.vat',
                              string="NIF")
    partner_phone = fields.Char(related='invoice_id.partner_id.phone',
                                string="Tlf", readonly=True)
    partner_email = fields.Char(related='invoice_id.partner_id.email',
                                string="Email", readonly=True)
    partner_street = fields.Char(related='invoice_id.partner_id.street',
                                 string="Calle", readonly=True)
    partner_zip = fields.Char(related='invoice_id.partner_id.zip',
                              string="CP", readonly=True)
    partner_city = fields.Char(related='invoice_id.partner_id.city',
                               string="Ciudad", readonly=True)
    partner_state = fields.Char(related='invoice_id.partner_id.state_id.name',
                                string="Provincia", readonly=True)
    categ_id = fields.Char(
        related='product_id.categ_id.display_name',
        string="Categoría interna", readonly=True)

    sale_order_lines = fields.Many2many('sale.order.line',
                                        'sale_order_line_invoice_rel',
                                        'invoice_line_id',
                                        'order_line_id',
                                        'Sale Order  Lines', readonly=True)

    margin_ptje = fields.Float(digits=(6, 2), string="Margen (%)",
                               compute='_get_margin_ptje')
    margin_base = fields.Float(digits=(6, 2), string="Margen",
                               compute='_get_margin_ptje')
    price_min = fields.Float(digits=(6, 2), string="Precio mínimo")
    margin_ptje_min = fields.Float(digits=(6, 2), string="Margen Min (%)",
                                   compute='_get_margin_ptje')
    margin_base_min = fields.Float(digits=(6, 2), string="Margen Min",
                                   compute='_get_margin_ptje')
    ref_product = fields.Char(related='product_id.default_code',
                              string="Cod producto", readonly=True)
    code_account = fields.Char(related='account_id.code', string="Cod cuenta",
                               readonly=True)
    invoice_number = fields.Char(related='invoice_id.number',
                                 string="Num factura",
                                 readonly=True)

    def _get_margin_ptje(self):
        for record in self:
            # Calculo margen en euros
            price_cost = record.purchase_price            
            price_cost_min = record.price_min
            margin_base = record.price_subtotal - (price_cost *
                                                   record.quantity)
            margin_base_min = record.price_subtotal - (price_cost_min *
                                                       record.quantity)
            # Calculo margen en %
            margen = 0
            margen_min = 0
            if record.price_subtotal != 0.0:
                margen = (margin_base / record.price_subtotal) * 100
                margen_min = (margin_base_min / record.price_subtotal) * 100
            
            # Escribo margen basado en coste
            record.margin_base = margin_base
            record.margin_base_min = margin_base_min
            # Escribo margen basado en precio mínimo
            record.margin_ptje_min = margen_min
            record.margin_ptje = margen
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        Cálculo del precio mínimo
        """
        res = super(AccountInvoiceLine, self)._onchange_product_id()
        if not self.product_id:
            return res
        min_price_pl = self.env.ref('indaws_nostrum_sport.pricelist_min_price')
        price_min = min_price_pl.get_product_price(
            self.product_id, self.quantity or 1.0, 
            self.invoice_id.partner_id)
        self.price_min = price_min
        self.purchase_price = self.product_id.standard_price
        return res


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    margin_ptje = fields.Float(digits=(6, 2), string="Margen (%)",
                               compute='_get_margin_ptje', store=True,
                               group_operator='avg')
    margin_base = fields.Float(digits=(6, 2), string="Margen",
                               compute='_get_margin_ptje', store=True)
    margin_ptje_min = fields.Float(digits=(6, 2), string="Margen Min(%)",
                                   compute='_get_margin_ptje')
    margin_base_min = fields.Float(digits=(6, 2), string="Margen Min",
                                   compute='_get_margin_ptje')


    partner_ref = fields.Char(related='partner_id.ref', string="Num cuenta",
                              readonly=True)
    partner_vat = fields.Char(related='partner_id.vat', string="NIF",
                              readonly=True)
    partner_phone = fields.Char(related='partner_id.phone', string="Tlf",
                                readonly=True)
    partner_email = fields.Char(related='partner_id.email', string="Email",
                                readonly=True)
    partner_zip = fields.Char(related='partner_id.zip', string="CP",
                              readonly=True)
    partner_city = fields.Char(related='partner_id.city', string="Ciudad",
                               readonly=True)
    partner_state = fields.Char(related='partner_id.state_id.name',
                                string="Provincia", readonly=True)

    def _recalcular_todo(self):
        records = self.env['account.invoice'].search([('type', '=', 'out_refund')])
        records._get_margin_ptje()

    @api.depends('invoice_line_ids', 'invoice_line_ids.purchase_price',
                 'invoice_line_ids.price_min', 'invoice_line_ids.quantity')
    def _get_margin_ptje(self):
        for record in self:
            purchase_total = 0.0
            purchase_total_min = 0.0
            for lin in record.invoice_line_ids:
                purchase_total += (lin.purchase_price * lin.quantity)
                purchase_total_min += (lin.price_min * lin.quantity)
            margen = 0
            margen_min = 0
            margin_base = record.amount_untaxed - purchase_total
            margin_base_min = record.amount_untaxed - purchase_total_min
            if record.type == 'out_refund':
                margin_base = margin_base*(-1)
                margin_base_min = margin_base_min*(-1)
            if record.amount_untaxed != 0.0:
                margen = (margin_base / record.amount_untaxed) * 100
                margen_min = (margin_base_min / record.amount_untaxed) * 100
            record.margin_base = margin_base
            record.margin_ptje = margen
            record.margin_base_min = margin_base_min
            record.margin_ptje_min = margen_min

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        result = super(AccountInvoice, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for group in result:
            if 'margin_ptje' in fields and group['amount_untaxed_signed']:
                group['margin_ptje'] = (group['margin_base'] / group['amount_untaxed_signed']) * 100
        return result

class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    code_account = fields.Char(related='account_id.code', string="Cod cuenta",
                               readonly=True)
    # MIGRATION CAMBIADO CAMPO INVOICE POR INVOICE_ID
    invoice_number = fields.Char(related='invoice_id.number',
                                 string="Num factura",
                                 readonly=True)
    concepto_factura = fields.Char(string="Concepto",
                                   compute='_get_concepto_factura')
    # MIGRATION CAMBIADO CAMPO INVOICE POR INVOICE_ID
    base_factura = fields.Monetary(related='invoice_id.amount_untaxed',
                                   string="Base factura", readonly=True)

    def _get_concepto_factura(self):
        for record in self:
            concepto = ''
            if record.invoice:
                concepto = record.invoice.number
            if record.partner_id:
                concepto = concepto + ' ' + record.partner_id.name
            record.concepto_factura = concepto


class AccountInvoiceNostrum(models.Model):
    _name = "account.invoice.nostrum"

    date_ini = fields.Date(default=fields.Date.today, string='Fecha inicio',
                           required=True)
    date_fin = fields.Date(default=fields.Date.today, string='Fecha fin',
                           required=True)
    date_calc = fields.Datetime(default=fields.Date.today,
                                string='Fecha de cálculo', readonly=True)

    invoice_out = fields.Boolean("Facturas de cliente")
    invoice_refund_out = fields.Boolean("Facturas rectificativas de cliente")
    invoice_in = fields.Boolean("Facturas de proveedor")
    invoice_refund_in = fields.Boolean("Facturas rectificativas de proveedor")

    invoice_ids = fields.Many2many('account.invoice', string="Facturas",
                                   readonly=True)
    sale_ids = fields.Many2many('sale.order', string="Pedidos", readonly=True)
    pos_ids = fields.Many2many('pos.order', string="Pedidos", readonly=True)
    move_line_ids = fields.Many2many('account.move.line',
                                     string="Lineas de asiento",
                                     readonly=True)

    sale_line_ids = fields.Many2many('sale.order.line', string="Líneas ventas",
                                     readonly=True)
    purchase_line_ids = fields.Many2many('purchase.order.line',
                                         string="Líneas compras",
                                         readonly=True)

    @api.multi
    def action_confirm(self):
        self.date_calc = datetime.now()

        self.invoice_ids = None
        self.sale_ids = None
        self.move_line_ids = None
        self.sale_line_ids = None
        self.purchase_line_ids = None

        type_invoices = []
        if self.invoice_out is True:
            type_invoices.append('out_invoice')
        if self.invoice_refund_out is True:
            type_invoices.append('out_refund')
        if self.invoice_in is True:
            type_invoices.append('in_invoice')
        if self.invoice_refund_in is True:
            type_invoices.append('in_refund')

        state_sale_order = ['waiting_date', 'progress', 'manual',
                            'shipping_except', 'invoice_except', 'done']
        state_purchase_order = ['confirmed', 'approved', 'except_picking',
                                'except_invoice', 'done']
        # Calculos
        domain1 = [('date_invoice', '>=', self.date_ini),
                   ('date_invoice', '<=', self.date_fin),
                   ('type', 'in', type_invoices)]
        self.invoice_ids = self.env['account.invoice'].search(domain1)

        domain2 = [('date_order', '>=', self.date_ini),
                   ('date_order', '<=', self.date_fin),
                   ('state', 'in', state_sale_order)]
        self.sale_ids = self.env['sale.order'].search(domain2)

        domain3 = [('date_order', '>=', self.date_ini),
                   ('date_order', '<=', self.date_fin)]
        self.pos_ids = self.env['pos.order'].search(domain3)
        self.move_line_ids = None

        domain4 = [('order_id.date_order', '>=', self.date_ini),
                   ('order_id.date_order', '<=', self.date_fin),
                   ('order_id.state', 'in', state_purchase_order)]
        self.sale_line_ids = self.env['sale.order.line'].search(domain4)

        domain5 = [('order_id.date_order', '>=', self.date_ini),
                   ('order_id.date_order', '<=', self.date_fin),
                   ('order_id.state', 'in', state_purchase_order)]
        self.purchase_line_ids = self.env['purchase.order.line'].\
            search(domain5)

    @api.multi
    def action_open_invoices(self):
        ref_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_invoice_ids'
        action = self.env.ref(ref_name).read()[0]
        action['domain'] = [('id', 'in', self.invoice_ids.ids)]
        return action

    @api.multi
    def action_open_invoices_lines(self):
        r_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_invoice_line_ids'
        action = self.env.ref(r_name).read()[0]
        invoice_line_ids = []
        for elem in self.invoice_ids:
            for line in elem.invoice_line_ids:
                invoice_line_ids.append(line.id)
        action['domain'] = [('id', 'in', invoice_line_ids)]
        return action

    @api.multi
    def action_open_move_lines(self):
        r_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_move_line_ids'
        action = self.env.ref(r_name).read()[0]
        move_line_ids = []
        for elem in self.invoice_ids:
            for line in elem.move_id.line_id:
                move_line_ids.append(line.id)
        action['domain'] = [('id', 'in', move_line_ids)]
        return action

    @api.multi
    def action_open_sales(self):
        r_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_sale_ids'
        action = self.env.ref(r_name).read()[0]
        action['domain'] = [('id', 'in', self.sale_ids.ids)]
        return action

    @api.multi
    def action_open_pos(self):
        r_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_pos_ids'
        action = self.env.ref(r_name).read()[0]
        action['domain'] = [('id', 'in', self.pos_ids.ids)]
        return action

    @api.multi
    def action_open_sales_lines(self):
        r_name = 'indaws_nostrum_sport.act_invoice_nostrum_2_sale_order_line_ids'
        action = self.env.ref(r_name).read()[0]
        action['domain'] = [('id', 'in', self.sale_line_ids.ids)]
        return action

    @api.multi
    def action_open_purchases_lines(self):
        r_name = 'indaws_nostrum_sport.\
            act_invoice_nostrum_2_purchase_order_line_ids'
        action = self.env.ref(r_name).read()[0]
        action['domain'] = [('id', 'in', self.purchase_line_ids.ids)]
        return action
