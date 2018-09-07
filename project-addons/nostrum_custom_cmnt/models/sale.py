# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_term = fields.Many2one(required=True, readonly=False)
    payment_mode_id = fields.Many2one(required=True)
    phonecall_count = fields.Integer(related='partner_id.phonecall_count',
                                     string="Nº Calls")

    @api.multi
    def action_confirm(self):
        """
        Que no nos cree línea de envío.
        """
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            so.invoice_shipping_on_delivery = False
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 related='order_id.partner_id')
    date_order = fields.Datetime('Date Order', related='order_id.date_order')

    # FULL OVERWRITED TO AVOID SET DISCOUNT = 0 WHEN CHANGING QRT
    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty',
                  'tax_id')
    def _onchange_discount(self):
        # self.discount = 0.0  COMMENTED
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.order_id.pricelist_id and
                self.order_id.pricelist_id.
                discount_policy == 'without_discount' and
                self.env.user.has_group('sale.group_discount_per_so_line')):
            return

        context_partner = dict(self.env.context,
                               partner_id=self.order_id.partner_id.id,
                               date=self.order_id.date_order)
        pricelist_context = dict(context_partner, uom=self.product_uom.id)

        price, rule_id = self.order_id.pricelist_id.\
            with_context(pricelist_context).\
            get_product_price_rule(self.product_id,
                                   self.product_uom_qty or 1.0,
                                   self.order_id.partner_id)
        new_list_price, currency_id = self.with_context(context_partner).\
            _get_real_price_currency(self.product_id, rule_id,
                                     self.product_uom_qty,
                                     self.product_uom,
                                     self.order_id.pricelist_id.id)

        if new_list_price != 0:
            if self.order_id.pricelist_id.currency_id.id != currency_id:
                # we need new_list_price in the same currency as price,
                # which is in the SO's pricelist's currency
                new_list_price = self.env['res.currency'].\
                    browse(currency_id).with_context(context_partner).\
                    compute(new_list_price,
                            self.order_id.pricelist_id.currency_id)
            discount = (new_list_price - price) / new_list_price * 100
            if discount > 0:
                self.discount = discount
