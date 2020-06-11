# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from __builtin__ import type

import unicodedata
import re
import os

# optional python-slugify import (https://github.com/un33k/python-slugify)
try:
    import slugify as slugify_lib
except ImportError:
    slugify_lib = None

from odoo import http, api, models, fields
from odoo.tools import ustr

import datetime
CACHE_TIME = datetime.timedelta(seconds=60)


####################################################
# Slug API
####################################################

def slugify(s, max_length=None):
    """ Transform a string to a slug that can be used in a url path.
        This method will first try to do the job with python-slugify if present.
        Otherwise it will process string by stripping leading and ending spaces,
        converting unicode chars to ascii, lowering all chars and replacing spaces
        and underscore with hyphen "-".
        :param s: str
        :param max_length: int
        :rtype: str
    """
    s = ustr(s)
    if slugify_lib:
        # There are 2 different libraries only python-slugify is supported
        try:
            return slugify_lib.slugify(s, max_length=max_length)
        except TypeError:
            pass
    uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    slug_str = re.sub('[\W_]', ' ', uni).strip().lower()
    slug_str = re.sub('[-\s]+', '-', slug_str)

    return slug_str[:max_length]


####################################################
# Local classes
####################################################

class UrlsRedirect(http.Controller):

    @http.route(['/es/<path:path>', '/pt/<path:path>', '/fr/<path:path>'], type='http', auth='public', website=True)
    def search_product_by_slug(self, path, **kw):
        split = path.split('.html')
        direction = split[0]
        products_list = http.request.env['product.template']
        category_list = http.request.env['product.public.category']
        is_product = products_list.sudo().search([('slug', '=', direction)])
        is_category = category_list.sudo().search([('slug', '=', direction)])
        if is_product.id:
            identifier, name = is_product.id, is_product.display_name
            slugname = slugify(name or '').strip().strip('-')
            direction = "/shop/product/%s-%d" % (slugname, identifier)
            return http.local_redirect(
                direction,
                dict(http.request.httprequest.args),
                True,
                code='301'
            )
        elif is_category.id:
            identifier, name = is_category.id, is_category.name
            slugname = slugify(name or '').strip().strip('-')
            direction = "/shop/category/%s-%d" % (slugname, identifier)
            return http.local_redirect(
                direction,
                dict(http.request.httprequest.args),
                True,
                code='301'
            )
        else:
            return http.local_redirect('/%s' % path)

    @http.route(['/es/content/<path:path>', '/pt/content/<path:path>', '/fr/content/<path:path>'],
                type='http', auth='public', website=True)
    def text_page(self, path):
        split = path.split('.html')
        direction = '/page/' + split[0]
        return http.local_redirect(
            direction,
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/contacto', '/pt/contacto', '/fr/contacto'], type='http', auth='public', website=True)
    def contact_page(self):
        return http.local_redirect(
            '/page/contactus',
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/pedido-rapido', '/pt/pedido-rapido', '/fr/pedido-rapido'],
                type='http', auth='public', website=True)
    def cart_page(self):
        return http.local_redirect(
            '/shop/cart',
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/blog/<path:path>', '/pt/blog/<path:path>', '/fr/blog/<path:path>'], type='http', auth='public', website=True)
    def post_page(self, path):
        redirect_list = {
            '53_Curso-de-Introduccion-a-la-T\xe9cnica-EPI-con-Jo.html':
                'curso-de-introduccion-a-la-tecnica-epi-con-jose-manuel-sanchez-8-y-9-de-junio-1',
            '51_Promocion-FisioAgenda.html': 'promocion-fisioagenda-53',
            '48_PlanRenoveNewAge.html': 'conoce-el-plan-renove-52',
            '47_tipos-de-cremas-y-aceites-para-masaje.html': 'tipos-de-cremas-y-aceites-para-masajes-51',
            '46_hidratarse-y-alimentarse-en-una-maraton.html':
                'a-importancia-de-rehidratarte-y-alimentarte-durante-una-maraton-50',
            '45_roller-massager.html': 'roller-massager-descontracturante-49',
            '44_curso-chocoterapia.html': 'chocoterapia-una-alternativa-de-disfrutar-del-chocolate-sin-engordar-48',
            '43_horario-oto\xf1o-invierno.html': 'horario-otono-invierno-como-nos-afecta-47',
            '42_fisioterapia-electroterapia-2.html': 'electroterapia-parte-2-46',
            '41_Las-plantillas-son-un-milagro-para-muchos-run.html':
                'las-plantillas-son-un-milagro-para-muchos-runners-45',
            '40_roller.html': 'realmente-funcionan-los-famosos-rollers-44',
            '39_deporte-salud-cerebral.html': 'como-repercute-el-deporte-a-nuestro-cerebro-43',
            '38_masaje-tratamiento-terapeutico.html': 'masajes-cuando-recurrir-a-ellos-42',
            '37_consejos-para-dormir-mejor.html': 'consejos-para-dormir-bien-41',
            '36_tecnicas-electroterapia.html': 'electroterapia-parte-1-40',
            '35_deportes-oto\xf1o.html': 'los-deportes-del-otono-39',
            '34_Frio-o-calor-para-una-lesion-.html': 'frio-o-calor-para-una-lesion-38',
            '33_alimentacion-oto\xf1o.html': 'la-mejor-alimentacion-para-este-otono-37',
            '32_pilates.html': 'pilates-36',
            '31_acondiconar-tu-clinica.html': 'ahora-es-mas-facil-acondicionar-tu-clinica-35',
            '30_descubre-acupuntura-beneficios.html': 'descubre-la-acupuntura-y-sus-beneficios-34',
            '29_10consejos-evitar-lesionarse.html': '10-consejos-para-evitar-lesionarse-33',
            '28_precalentamiento-ejercicio.html': 'pautas-para-un-calentamiento-10-32',
            '27_dia-mundial-fisioterapia.html': 'dia-mundial-de-la-fisioterapia-maximiza-tu-potencial-31',
            '26_aplicaciones-salud-deporte.html': 'aplicaciones-de-salud-y-deporte-30',
            '25_alimentos-mas-saludables.html': 'alimentos-mas-saludables-29',
            '24_beneficios-kinesiotape.html': 'que-es-el-kinesiotape-28',
            '23_accesorios-pilates-playa.html': '5-accesorios-de-pilates-que-puedes-usar-en-la-playa-27',
            '22_cremas-aceites-masajes.html': 'cremas-y-aceites-indicados-para-masajes-26',
            '21_patologias-aquiles.html': 'patologias-que-se-incrementan-en-verano-tendinitis-aquilea-25',
            '19_seminario-magnetoterapia.html': 'seminario-magnetoterapia-23',
            '18_lumbago-que-es-y-como-tratarlo.html': 'lumbago-que-es-y-como-tratarlo-22',
            '17_LESIONES-MUSCULARES-M\xc1S-FRECUENTES.html': 'lesiones-musculares-mas-frecuentes-21',
            '16_sindrome-del-tunel-carpiano.html': 'sindrome-del-tunel-carpiano-en-el-deporte-20',
            '20_prevenir-la-deshidratacion-deporte.html': 'prevenir-la-deshidratacion-en-el-deporte-24',
            '15_cambios-estacionales.html': 'los-cambios-estacionales-19',
            '14_esguinces-de-tobillo-parte-II.html': 'esguinces-de-tobillo-ii-rehabilitacion-18',
            '13_esguinces-de-tobillo-parte-I.html': 'esguinces-de-tobillo-i-tratamientos-17',
            '12_masaje-despues-del-deporte.html': 'masaje-despues-del-deporte-16',
            '11_mejora-tu-rendimiento.html': 'que-puedo-hacer-yo-para-ser-mejor-deportista-y-sentirme-pletorico-15',
            '10_sorteo.html': 'sorteo-de-2-plazas-para-el-curso-de-kinetic-control-14',
            '9_metedo-mcconnell.html': 'metodo-mcconnell-13',
            '8_minimotion.html': 'minimotion-12',
            '7_terapias-orientales-gua-sha.html': 'terapias-orientales-gua-sha-11',
        }
        origin = redirect_list.get(path, False)

        if origin is not False:
            way = '/blog/blog-1/post/' + origin
            return http.local_redirect(
                way,
                dict(http.request.httprequest.args),
                True,
                code='301'
            )
        else:
            return http.local_redirect('/blog/blog-1')

    @http.route(['/', '/pt/', '/fr/'], type='http', auth='public', website=True)
    def start_page(self):
        return http.local_redirect(
            '/shop',
            dict(http.request.httprequest.args),
            True,
            code='301'
        )


class FaviconRoot(http.Controller):

    @http.route('/favicon.ico', type='http', auth="none")
    def favicon_redirect(self):
        filename = '/web/image/website/1/favicon/'
        return http.request.env['ir.http'].reroute(filename)


class ManifestRoot(http.Controller):

    def _auto_create(self, source, destination, mimetype):
        attachment = http.request.env['ir.attachment'].sudo()
        cache_content = None

        def create_file(url, content, mimetype):
            return attachment.create({
                'datas': content.encode('base64'),
                'mimetype': mimetype,
                'type': 'binary',
                'name': url,
                'url': url,
            })

        # Search in the cache
        domain = [('url', '=', destination), ('type', '=', 'binary')]
        in_cache = attachment.search(domain, limit=1)
        if in_cache:
            create_date = fields.Datetime.from_string(in_cache.create_date)
            delta = datetime.datetime.now() - create_date
            if delta < CACHE_TIME:
                cache_content = in_cache.datas.decode('base64')

        if not cache_content:
            # Remove all old files
            old_files = attachment.search(domain)
            old_files.unlink()

            # Create new file (attachment)
            rel_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = rel_path + source
            file_read = open(file_path)
            content = file_read.read()
            create_file(destination, content, mimetype)
        else:
            content = cache_content

        return http.request.make_response(content, [('Content-Type', mimetype)])

    @http.route('/manifest.json', type='http', auth="none")
    def manifest_redirect(self):
        return self._auto_create('/static/manifest.json', '/manifest.json', 'application/json;charset=utf-8')

    @http.route('/sw.js', type='http', auth="none")
    def sw_redirect(self):
        return self._auto_create('/static/js/sw.js', '/sw.js', 'application/javascript;charset=utf-8')
