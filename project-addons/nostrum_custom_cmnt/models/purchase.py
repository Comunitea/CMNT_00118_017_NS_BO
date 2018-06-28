# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


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
        if not seller and self.product_id and not self.price_unit:
            cost = self.product_id.standard_price
            price_unit = self.product_id.uom_po_id.\
                _compute_price(cost, self.product_id.uom_po_id)
            self.price_unit = price_unit
        return res
