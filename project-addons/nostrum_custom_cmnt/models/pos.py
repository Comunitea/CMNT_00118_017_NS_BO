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

            if order.invoice_id:
                vals = {}
                if pm:
                    vals.update({'payment_mode_id': pm})
                # Get commercial of partner
                if order.invoice_id.partner_id.user_id:
                    vals['user_id'] = order.invoice_id.partner_id.user_id.id
                if vals:
                    order.invoice_id.write(vals)

                # Recompute commissions:
                order.invoice_id.recompute_lines_agents()
        return res

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        if res['partner_id']:
            partner = self.env['res.partner'].browse(res['partner_id'])
            if partner.user_id:
                res['user_id'] = partner.user_id.id
        return res
