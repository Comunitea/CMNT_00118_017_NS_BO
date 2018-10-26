# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class product_public_category(models.Model):
    _inherit = "product.public.category"

    slug = fields.Char('Category old URL', help="Old category URL for redirection")
