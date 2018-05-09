# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_term_id = fields.Many2one(required=True, readonly=False)
