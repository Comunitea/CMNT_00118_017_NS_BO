# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_term = fields.Many2one(required=True, readonly=False)
    payment_mode_id = fields.Many2one(required=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 related='order_id.partner_id')
    date_order = fields.Datetime('Date Order', related='order_id.date_order')
