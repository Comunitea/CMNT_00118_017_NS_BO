# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    cost = fields.Float('Cost', related="product_id.standard_price",
                        readonly=True)
    state = fields.Selection('State', related='order_id.state')
