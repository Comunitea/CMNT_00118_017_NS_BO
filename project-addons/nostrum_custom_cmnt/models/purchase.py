# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_term_id = fields.Many2one(required=True, readonly=False)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _onchange_quantity(self):
        res = super(PurchaseOrderLine, self)._onchange_quantity()
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)
        # Set cost to purchase price if not seller and price unit defined.
        if self.product_id and (not seller or not self.price_unit):
            cost = self.product_id.standard_price
            price_unit = self.product_id.uom_po_id.\
                _compute_price(cost, self.product_id.uom_po_id)
            self.price_unit = price_unit
        return res

    current_stock_days = fields.Float('Stock days', readonly=True)

    @api.multi
    def update_current_stock_days(self):
        self.ensure_one()
        product = self.product_id

        units_by_month = product.last_year_unit_sales / 12.0
        if units_by_month:
            stock_months = \
                (product.qty_available + self.product_qty) / units_by_month
            stock_days = stock_months * 30.0
            self.write({'current_stock_days': stock_days})
    
    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
        res.update_current_stock_days()
        return res
    
    @api.multi
    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if 'product_qty' in vals:
            for line in self:
                line.update_current_stock_days()
        return res