# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api

class SaleCommissionMixin(models.AbstractModel):
    _inherit = 'sale.commission.mixin'

    @api.model
    def _prepare_agents_vals(self):
        """Utility method for getting agents of a partner."""
        res = super(SaleCommissionMixin, self).\
            _prepare_agents_vals()
        partner = False
        if self.env.context.get('partner_id'):
            partner = self.env['res.partner'].browse(
                self.env.context['partner_id'])
        if partner and self.product_id.commission_id:
            res = []
            for agent in self.object.agents:
                rec.append((0, 0, {
                    'agent': agent.id,
                    'commission': self.product_id.commission_id.id,
                }))
        return res
    
    @api.model
    def create(self, vals):
        res =  super(SaleCommissionMixin, self).create(vals)
        if 'agents' in vals and res.product_id.commission_id:
            res.mapped('agents').write(
                {'commission': res.product_id.commission_id.id })
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleCommissionMixin, self).write(vals)
        for line in self:
            if self.product_id.commission_id:
                line.mapped('agents').write(
                    {'commission': line.product_id.commission_id.id })
        return res


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
    
    @api.onchange('agent')
    def onchange_agent(self):
        """
        Get specific commission to the agent
        """
        super(SaleCommissionLineMixin, self).onchange_agent()
        if self.object_id.product_id.commission_id:
            self.commission = self.object_id.product_id.commission_id.id