# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import datetime
from datetime import date
from odoo import http, api, models, fields
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.models.website import slug

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)


class SitemapGenerate(Website):

    @http.route('/sitemap.xml', type='http', auth="public", website=True)
    def sitemap_generate(self):
        attachment = request.env['ir.attachment'].sudo()
        view = request.env['ir.ui.view'].sudo()
        mimetype = 'application/xml;charset=utf-8'
        sitemap_content = ''
        cache_content = None

        dom = [('url', '=', '/sitemap.xml'), ('type', '=', 'binary')]
        sitemap = attachment.search(dom, limit=1)
        if sitemap:
            create_date = fields.Datetime.from_string(sitemap.create_date)
            delta = datetime.datetime.now() - create_date
            if delta < SITEMAP_CACHE_TIME:
                cache_content = sitemap.datas.decode('base64')

        def create_sitemap(url, content):
            return attachment.create({
                'datas': content.encode('base64'),
                'mimetype': mimetype,
                'type': 'binary',
                'name': url,
                'url': url,
            })

        def create_one(loc, lastmod, changefreq, image, priority):
            return view.render_template('theme_adds.sitemap_tpl', {
                'loc': loc,
                'lastmod': lastmod,
                'changefreq': changefreq,
                'image': image,
                'priority': priority
            })

        if not cache_content:
            # Remove all old sitemaps
            sitemaps = attachment.search(dom)
            sitemaps.unlink()

            # Create new sitemap
            today = date.today()
            first_day = date(today.year, today.month, 1)
            root = request.httprequest.url_root

            # Add favicon.ico
            sitemap_content += create_one(root + 'favicon.ico', first_day, 'weekly', root + 'favicon.ico', '0.5')

            # Add robots.txt
            sitemap_content += create_one(root + 'robots.txt', first_day, 'weekly', '', '0.5')

            # Add home page
            image = '%stheme_adds/static/img/logo-head.png' % root
            sitemap_content += create_one(root + 'shop', first_day, 'weekly', image, '0.5')

            # Add product public categories
            domain = [('website_published', '=', True)]
            category_ids = request.env['product.public.category'].sudo().search(domain)

            for r in category_ids:
                loc = '%scategory/%s' % (root, r.slug) if r.slug else '%sshop/category/%s' % (root, slug(r))
                if r.image_medium:
                    image = '%sweb/image?model=product.public.category&id=%s&field=image_medium' % (root, r.id)
                else:
                    image = ''
                sitemap_content += create_one(loc, r.write_date[:-9], 'weekly', image, '0.5')

            # Add active and published products
            domain = [('sale_ok', '=', True)]
            domain += [('active', '=', True)]
            domain += [('website_published', '=', True)]
            product_ids = request.env['product.template'].sudo().search(domain)

            for r in product_ids:
                loc = '%sproduct/%s' % (root, r.slug) if r.slug else '%sshop/product/%s' % (root, slug(r))
                image = '%sweb/image/product.template/%s/image/' % (root, r.id) if r.image else ''
                sitemap_content += create_one(loc, r.write_date[:-9], 'weekly', image, '0.5')

            # Sitemap generation
            content = view.render_template('theme_adds.sitemap_wrap', {'content': sitemap_content})
            create_sitemap('/sitemap.xml', content)
        else:
            content = cache_content

        return request.make_response(content, [('Content-Type', mimetype)])
