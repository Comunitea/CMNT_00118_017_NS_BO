
# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class RecomputeSalePriceMin(models.TransientModel):

    _name = 'recompute.sale.price.min'

    @api.multi
    def recompute_price_min(self):
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        orders = self.env['sale.order'].browse(active_ids)
        min_price_pl = self.env.ref('indaws_nostrum_sport.pricelist_min_price')
        for line in orders.mapped('order_line'):
            price_min = min_price_pl.get_product_price(
                line.product_id, line.product_uom_qty or 1.0, 
                line.order_id.partner_id)
            line.price_min = price_min
        return


class RecomputeInvoicePriceMin(models.TransientModel):

    _name = 'recompute.invoice.price.min'

    @api.multi
    def recompute_price_min(self):
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        invoices = self.env['account.invoice'].browse(active_ids)
        min_price_pl = self.env.ref('indaws_nostrum_sport.pricelist_min_price')
        for line in invoices.mapped('invoice_line_ids'):
            price_min = min_price_pl.get_product_price(
                line.product_id, line.quantity or 1.0, 
                line.invoice_id.partner_id)
            line.price_min = price_min
        return
