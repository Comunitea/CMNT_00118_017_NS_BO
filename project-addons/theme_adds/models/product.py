# -*- coding: utf-8 -*-
#
# Add new Tag field used for submenu shop.
# Submenu shop only shows Tags when field marked is True
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTag(models.Model):
    _inherit = 'product.tag'

    marked = fields.Boolean('Marked')
    tag_color = fields.Selection([('default', 'Green'),
                                  ('red', 'Red'),
                                  ('yellow', 'Yellow'),
                                  ('blue', 'Blue'),
                                  ('gray', 'Gray')], 'Tag label color', default='default')


class ProductDescription(models.Model):
    _inherit = 'product.template'

    description_short = fields.Text('Short description', help="Short description for product page", strip_style=True)
    description = fields.Html('Content', strip_style=True)
