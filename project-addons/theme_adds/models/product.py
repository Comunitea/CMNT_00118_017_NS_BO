# -*- coding: utf-8 -*-
#
# Add new Tag field used for submenu shop.
# Submenu shop only shows Tags when field marked is True
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


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
    slug = fields.Char(_("SEO Old URL"), help=_("Prestashop Old Product URL for redirection of Google SEO"))
    hide_website_price = fields.Boolean(_("Hide Website Price"), default=False,
                                        help=_("If selected, hide price and add to cart button"))
    product_meta_title = fields.Char("SEO Meta Title", translate=True)
    product_meta_description = fields.Text("SEO Meta Description", translate=True)
    product_meta_keywords = fields.Char("SEO Meta Keywords", translate=True)
