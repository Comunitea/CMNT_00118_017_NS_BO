# -*- coding: utf-8 -*-
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Website(models.Model):
    _inherit = 'website'

    """
        Get only product tags marked as True to show in shop submenu
    """
    def get_product_tags_marked(self):
        tag_pool = self.env["product.tag"]
        domain = [('marked', '=', True)]
        tag_objs = tag_pool.sudo().search(domain)
        return tag_objs
