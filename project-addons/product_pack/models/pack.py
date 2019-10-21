# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __odoo__.py file in root directory
##############################################################################
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class ProductPack(models.Model):
    _name = 'product.pack.line'
    _rec_name = 'product_id'

    parent_product_id = fields.Many2one(
        'product.product',
        'Parent Product',
        ondelete='cascade',
        required=True)
    quantity = fields.Float(
        'Quantity',
        required=True,
        default=1.0,
        digits=dp.get_precision('Product UoS'))
    product_id = fields.Many2one(
        'product.product',
        'Product',
        ondelete='cascade',
        required=True)
    discount = fields.Float(
        'Discount (%)',
        digits=dp.get_precision('Discount'))

    @api.multi
    def get_sale_order_line_vals(self, line, order):
        self.ensure_one()
        # pack_price = 0.0
        subproduct = self.product_id
        quantity = self.quantity * line.product_uom_qty

        taxes = order.fiscal_position_id.map_tax(
            subproduct.taxes_id)
        tax_id = [(6, 0, taxes.ids)]

        # POST MIGRATION, NO HAY UOS
        # if subproduct.uos_id:
        #     uos_id = subproduct.uos_id.id
        #     uos_qty = quantity * subproduct.uos_coeff
        # else:
        #     uos_id = False
        #     uos_qty = quantity

        # if pack is fixed price or totlice price we don want amount on
        # pack lines
        if line.product_id.pack_price_type in [
                'fixed_price', 'totalice_price']:
            price = 0.0
            discount = 0.0
            cost = 0.0
            price_min = 0.0
        else:
            pricelist = order.pricelist_id.id
            price = self.env['product.pricelist'].price_get(
                subproduct.id, quantity,
                order.partner_id.id, context={
                    'uom': subproduct.uom_id.id,
                    'date': order.date_order})[pricelist]
            discount = self.discount
            cost = subproduct.standard_price
            min_price_pl = self.env.ref(
                'indaws_nostrum_sport.pricelist_min_price')
            price_min =  min_price_pl.get_product_price(
                subproduct.id, quantity,
                subproduct, line.product_uom_qty or 1.0, 
                order.partner_id.id)


        # Obtain product name in partner's language
        if order.partner_id.lang:
            subproduct = subproduct.with_context(
                lang=order.partner_id.lang)
        subproduct_name = subproduct.name

        vals = {
            'order_id': order.id,
            'name': '%s%s' % (
                '> ' * (line.pack_depth + 1), subproduct_name
            ),
            # 'delay': subproduct.sale_delay or 0.0,
            'product_id': subproduct.id,
            # 'procurement_ids': (
            #     [(4, x.id) for x in line.procurement_ids]
            # ),
            'price_unit': price,
            'tax_id': tax_id,
            'address_allotment_id': False,
            'product_uom_qty': quantity,
            'product_uom': subproduct.uom_id.id,
            # 'product_uos_qty': uos_qty,  NO HAY UOS (postmigration)
            # 'product_uos': uos_id,  NO HAY UOS (postmigration)
            'product_packaging': False,
            'discount': discount,
            'number_packages': False,
            'th_weight': False,
            'state': 'draft',
            'pack_parent_line_id': line.id,
            'is_component': True,
            'pack_depth': line.pack_depth + 1,
            'purchase_price': cost,
            'price_min': price_min
        }
        return vals
