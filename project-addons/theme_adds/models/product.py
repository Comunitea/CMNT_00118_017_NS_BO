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


class ProductCustom(models.Model):
    _inherit = 'product.template'

    description_short = fields.Text(_("Short product description"), help=_("Short description for product page"), strip_style=True)
    description = fields.Html(_("Full product description"), strip_style=True)
    slug = fields.Char(_("Product old URL Website"), help=_("Old website product URL for redirection of Google SEO"))
    hide_website_price = fields.Boolean(_("Hide Website Price"), default=False,
                                        help=_("If selected, hide price and add to cart button"))
