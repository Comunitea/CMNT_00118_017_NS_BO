# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def action_pos_order_invoice(self):
        res = super(PosOrder, self).action_pos_order_invoice()
        pm = False
        for order in self:
            if order.statement_ids and order.statement_ids[0].journal_id:
                if order.statement_ids[0].journal_id.payment_mode_id:
                    pm = order.statement_ids[0].journal_id.payment_mode_id.id

            if order.invoice_id and pm:
                order.invoice_id.write({'payment_mode_id': pm})
        return res
