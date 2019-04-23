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


class ProductCustom(models.Model):
    _inherit = 'product.template'

    description_short = fields.Text(_("Short product description"), help=_("Short description for product page"),
                                    strip_style=True)
    description = fields.Html(_("Full product description"), strip_style=True)
    slug = fields.Char(_("Friendly URL"), help=_("Friendly URL for SEO"))
    hide_website_price = fields.Boolean(_("Hide Website Price"), default=False,
                                        help=_("If selected, hide price and add to cart button"))
    product_meta_title = fields.Char("SEO Meta Title", translate=True)
    product_meta_description = fields.Text("SEO Meta Description", translate=True)
    product_meta_keywords = fields.Char("SEO Meta Keywords", translate=True)

    def slug_validation(self, value):
        # Unicode validation
        uni = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[\W_]', ' ', uni).strip().lower()
        value = re.sub('[-\s]+', '-', value)
        value = value[:60]

        # Check if this SLUG value already exists in any product or category
        it_exists = self.sudo().search([('slug', '=', value)], limit=1).id
        if it_exists and not it_exists == self.id:
            # Add random URL part
            value = '%s-%d' % (value, random.randint(0, 999))
        return value

    @api.multi
    def write(self, values):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        for product in self:
            has_slug = values.get('slug', False)
            if not has_slug or has_slug == '':
                # If slug not exists or is empty -> create from product name & id and validate
                if not product.slug:
                    new_slug = '%s-%s' % (product.name, product.id)
                    slug = product.slug_validation(new_slug)
                else:
                    slug = product.slug_validation(product.slug)
            else:
                # If slug exists -> validate
                slug = product.slug_validation(has_slug)
            # Write
            values.update({
                'slug': slug,
                'url_presupuesto': '%s/product/%s' % (base_url, slug)
            })
            super(ProductCustom, product).write(values)
            values.pop('slug')
            values.pop('url_presupuesto')
        return True

    @api.model
    def create(self, values):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        has_slug = values.get('slug', False)
        if not has_slug or has_slug == '':
            # If slug isn't established -> create from product name
            new_slug = values['name']
            slug = self.slug_validation(new_slug)
        else:
            # If slug is established -> validate
            slug = self.slug_validation(has_slug)
        # Create
        values.update({
            'slug': slug,
            'url_presupuesto': '%s/product/%s' % (base_url, slug)
        })
        return super(ProductCustom, self).create(values)


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
