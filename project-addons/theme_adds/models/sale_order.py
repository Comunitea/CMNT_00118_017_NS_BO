import logging

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_web_comment = fields.Text('Order web comment')

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
