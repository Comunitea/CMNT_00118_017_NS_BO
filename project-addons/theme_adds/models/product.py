# -*- coding: utf-8 -*-
#
# Add new Tag field used for submenu shop.
# Submenu shop only shows Tags when field marked is True
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import unicodedata
import re
import random
from odoo import api, models, fields, _
import odoo.addons.decimal_precision as dp


class ProductTag(models.Model):
    _inherit = 'product.tag'

    marked = fields.Boolean('Marked')
    tag_color = fields.Selection([('default', 'Green'),
                                  ('red', 'Red'),
                                  ('yellow', 'Yellow'),
                                  ('blue', 'Blue'),
                                  ('gray', 'Gray')], 'Tag label color', default='default')
    website_sequence = fields.Integer('Website Sequence', default=lambda self: self._default_website_sequence(),
                                      help=_("Choose the display order in the Website"))

    def _default_website_sequence(self):
        self._cr.execute("SELECT MIN(website_sequence) FROM %s" % self._table)
        min_sequence = self._cr.fetchone()[0]
        return min_sequence and min_sequence - 1 or 10


class Product(models.Model):
    _inherit = "product.product"

    website_discount_price = fields.Float('Website Discount Price', compute='_website_price',
                                          digits=dp.get_precision('Product Price'))

    def _website_price(self):
        super(Product, self)._website_price()
        qty = self._context.get('quantity', 1.0)
        partner = self.env.user.partner_id
        current_website = self.env['website'].get_current_website()
        pricelist = current_website.get_current_pricelist()
        company_id = current_website.company_id
        context = dict(self._context, pricelist=pricelist.id, partner=partner)
        self2 = self.with_context(context) if self._context != context else self

        ret = self.env.user.has_group('sale.group_show_price_subtotal') and 'total_excluded' or 'total_included'
        for p, p2 in zip(self, self2):
            taxes = partner.property_account_position_id.map_tax(
                p.taxes_id.sudo().filtered(lambda x: x.company_id == company_id))
            discount_price = p2.price / (1 + (taxes.amount/100))
            p.website_discount_price = taxes.compute_all(discount_price, pricelist.currency_id, quantity=qty,
                                                         product=p2, partner=partner)[ret]
