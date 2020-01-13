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

    @api.model
    def _get_website_data(self, order):
        
        values = super(SaleOrder, self)._get_website_data(order)
        
        product_ids = order.website_order_line.mapped('product_id')

        cart_type = self._compute_cart_type(product_ids)
                    
        if len(cart_type) == 1 and cart_type[0].encode('ascii', 'ignore') == 'service':
            
            values.update({
                'only_services': True
            })
        
        return values

    @api.multi
    def _compute_cart_type(self, products):
        cart_type = []
        for product in products:
            if product.type not in cart_type:
                cart_type.append(product.type)

        return cart_type