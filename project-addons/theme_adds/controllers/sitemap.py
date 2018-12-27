# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date
from odoo import http, api, models
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.models.website import slug


class SitemapGenerate(Website):

    @http.route('/sitemap.xml', type='http', auth="public", website=True)
    def sitemap_generate(self):
        attachment = request.env['ir.attachment'].sudo()
        view = request.env['ir.ui.view'].sudo()
        mimetype = 'application/xml;charset=utf-8'
        sitemap_content = ''

        def create_sitemap(url, content):
            return attachment.create({
                'datas': content.encode('base64'),
                'mimetype': mimetype,
                'type': 'binary',
                'name': url,
                'url': url,
            })

        # Add home page to sitemap
        today = date.today()
        first_day = date(today.year, today.month, 1)
        sitemap_content += view.render_template('theme_adds.sitemap_tpl', {
            'loc': request.httprequest.url_root + 'shop',
            'lastmod': first_day,
            'changefreq': 'weekly',
            'priority': '0.5'
        })

        # Add categories to sitemap
        domain = [('website_published', '=', True)]
        category_ids = request.env['product.public.category'].sudo().search(domain)

        for r in category_ids:
            values = {
                'loc': request.httprequest.url_root + 'shop/category/' + slug(r),
                'lastmod': r.write_date[:-9],
                'changefreq': 'weekly',
                'priority': '0.5'
            }
            sitemap_content += view.render_template('theme_adds.sitemap_tpl', values)

        # Add active and published products to sitemap
        domain = [('sale_ok', '=', True)]
        domain += [('active', '=', True)]
        domain += [('website_published', '=', True)]
        product_ids = request.env['product.template'].sudo().search(domain)

        for r in product_ids:
            values = {
                'loc': request.httprequest.url_root + 'shop/product/' + slug(r),
                'lastmod': r.write_date[:-9],
                'changefreq': 'weekly',
                'priority': '0.5'
            }
            sitemap_content += view.render_template('theme_adds.sitemap_tpl', values)

        # Sitemap generation
        content = view.render_template('theme_adds.sitemap_wrap', {'content': sitemap_content})
        create_sitemap('/sitemap.xml', content)

        return request.make_response(content, [('Content-Type', mimetype)])
