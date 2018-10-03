# -*- coding: utf-8 -*-
#
# Add new Tag field used for submenu shop.
# Submenu shop only shows Tags when field marked is True
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import http
from odoo.addons.clarico_shop.controllers.main import claricoShop
from odoo.http import request
#
#
class claricoShopCustom(claricoShop):

    """
        Change default search order
    """
    def _get_search_order(self, post):
        return '%s, id desc' % post.get('order', 'website_sequence asc')

    """
        Change default products to show in shop by ir.config_parameter
    """
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        if not 'ppg' in request.httprequest.args:
            IrConfigParam = request.env['ir.config_parameter']
            ppg = int(IrConfigParam.sudo().get_param('default_products_to_show', 8))

        return super(claricoShopCustom, self).shop(page=page, category=category, search=search, ppg=ppg, **post)

