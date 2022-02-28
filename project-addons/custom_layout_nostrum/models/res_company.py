# -*- coding: utf-8 -*-
# © 2022 Comunitea - Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models, _


class Company(models.Model):
    _inherit = "res.company"

    promotional_row = fields.Boolean(string="Promotional row", help="Adds a promotional row in the report layouts.", default=False)
    product_ids = fields.Many2many(comodel_name='product.product', string='Products to show', help="You can only add four products.")
    description_footer = fields.Html(_("Promotional footer description"), strip_style=True)
   