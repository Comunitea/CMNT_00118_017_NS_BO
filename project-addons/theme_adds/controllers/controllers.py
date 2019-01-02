# -*- coding: utf-8 -*-
#
# Add new Tag field used for submenu shop.
# Submenu shop only shows Tags when field marked is True
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import http
from odoo.http import request
from odoo.addons.clarico_shop.controllers.main import claricoShop
from odoo.addons.clarico_cart.controllers.main import claricoClearCart


class ClaricoShopCustom(claricoShop):

    """
        Change default search order
    """
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        return '%s , id asc' % post.get('order', 'website_sequence asc')

    """
        Change default products to show in shop start page
    """
    def _get_search_domain(self, search, category, attrib_values, price_vals = {}):

        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                    ('brand_ept_id.name', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if price_vals:
            domain += [('list_price', '>=', price_vals.get('min_val')), ('list_price', '<=', price_vals.get('max_val'))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if value[0] == 0:
                    ids.append(value[1])
                    domain += [('brand_ept_id.id', 'in', ids)]
                elif not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        tag_id = request.httprequest.args.get('tags')
        is_search = request.httprequest.args.get('search')

        if not category and not tag_id and not is_search:
            domain += [(u'tag_ids', u'ilike', u'Productos Destacados')]

        return domain

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

        if category and category.slug:
            return http.local_redirect(
                '/category/%s' % category.slug,
                dict(http.request.httprequest.args),
                True,
                code='301'
            )

        return super(ClaricoShopCustom, self).shop(page=page, category=category, search=search, ppg=ppg, **post)

    @http.route('/category/<path:path>', type='http', auth='public', website=True)
    def _shop(self, path, page=0, category=None, search='', ppg=False, **post):
        category_list = http.request.env['product.public.category']
        category = category_list.sudo().search([('slug', '=', path)], limit=1)
        if category:
            return super(ClaricoShopCustom, self).shop(page=page, category=category, search=search, ppg=ppg, **post)


class ClaricoClearCartCustom(claricoClearCart):

    """
        Clear cart including selected Payment Method and entire sale order to prevent errors
    """
    @http.route(['/shop/clear_cart'], type='json', auth="public", methods=['POST'], website=True)
    def clear_cart(self, **kw):
        order = request.website.sale_get_order(force_create=1)
        order.sudo().write({'payment_acquirer_id': False})
        order.sudo().unlink()

