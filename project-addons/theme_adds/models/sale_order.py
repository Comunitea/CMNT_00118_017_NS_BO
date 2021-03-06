import logging

from odoo import api, fields, models

import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_web_comment = fields.Text('Order web comment')
    no_digital_products_total = fields.Float(
        compute='_compute_no_digital_products_total',
        digits=dp.get_precision('Account'))
    amount_free_delivery = fields.Float(
        compute='_compute_amount_free_delivery',
        digits=dp.get_precision('Account'))

    @api.multi
    def _cart_find_product_line(self, product_id=None, line_id=None, **kwargs):
        self.ensure_one()

        product = self.env['product.product'].browse(product_id)

        domain = [('order_id', '=', self.id), ('product_id', '=', product_id)]
        if line_id:
            domain += [('id', '=', line_id)]

        # Product packs control
        if product and not product.pack and self.order_line.filtered(lambda r: r.pack_parent_line_id):
            products = self.order_line.filtered(
                lambda r: not r.pack_parent_line_id and not r.product_id.pack).mapped('product_id')
            for p in products:
                if p.id == product_id:
                    domain += [('price_unit', '!=', 0)]
                    return self.env['sale.order.line'].sudo().search(domain)

            return self.env['sale.order.line']

        # split lines with the same product if it has untracked attributes
        if product and product.mapped('attribute_line_ids').filtered(
                lambda r: not r.attribute_id.create_variant) and not line_id:
            return self.env['sale.order.line']

        return self.env['sale.order.line'].sudo().search(domain)

    @api.model
    def _get_website_data(self, order):
        values = super(SaleOrder, self)._get_website_data(order)
        only_services = all(line.product_id.type in ('service', 'digital') for line in
                            order.website_order_line.filtered(lambda x: not x.payment_fee_line))
        values.update({
            'only_services': only_services
        })
        return values

    @api.multi
    def delivery_set(self):
        only_services = all(line.product_id.type in ('service', 'digital') for line in
                            self.website_order_line.filtered(lambda x: not x.payment_fee_line))
        if only_services:
            self._delivery_unset()
            self.carrier_id = None
        else:
            return super(SaleOrder, self).delivery_set()

    @api.multi
    def _compute_no_digital_products_total(self):
        """
        Exclude digital and service products that are parts of pack from compute total_amount in order
        because products there are not really sent cannot be compute on delivery cost.
        There are included services products that are a service but there are a pack because there are a service
        only to improve sale and they are really sent.
        """
        for order in self:
            order.no_digital_products_total = sum(
                line.price_total for line in order.order_line.filtered(
                    lambda x: x.product_id.type not in ('service', 'digital') or (
                            x.product_id.type in ('service', 'digital') and x.product_id.pack)))

    @api.multi
    def _compute_amount_free_delivery(self):
        """
        Amount to get free delivery.
        """
        amount_to_get_free_delivery = 99.01
        for order in self:
            order.amount_free_delivery = amount_to_get_free_delivery - order.no_digital_products_total

    @api.model
    def _message_get_auto_subscribe_fields(self, updated_fields, auto_follow_fields=None):
        """
            Hook for user can decide it if receive or not auto subscribe fields by notify_email option
        """
        if auto_follow_fields is None:
            auto_follow_fields = ['user_id']
        user_field_lst = []
        for name, field in self._fields.items():
            if name in auto_follow_fields and name in updated_fields and getattr(field, 'track_visibility', False) \
                    and field.comodel_name == 'res.users':
                # New condition by notify email
                if eval('self.' + name).notify_email != 'none':
                    user_field_lst.append(name)
        return user_field_lst
