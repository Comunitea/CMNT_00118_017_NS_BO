# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class SaleCommissionLineMixin(models.AbstractModel):
    _inherit = 'sale.commission.line.mixin'

    @api.multi
    def _get_commission_amount(
            self, commission, subtotal, commission_free, product, quantity):
        new_subtotal = subtotal
        line = self.object_id
        if line._name == 'account.invoice.line' and \
                commission.amount_base_type == 'min_price':
            new_subtotal = subtotal - (line.price_min * quantity)
        return super(SaleCommissionLineMixin, self)._get_commission_amount(
            commission, new_subtotal, commission_free, product, quantity)