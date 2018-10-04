# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from __builtin__ import type

from odoo import http

class UrlsRedirect(http.Controller):

    # @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    # def product(self, product):
    #     origin = http.request.httprequest.path
    #     split = origin.split('/')

    @http.route(['/es/content/<path:path>'], type='http', auth='public', website=True)
    def text_page(self, path):
        split = path.split('.html')
        direction = '/page/' + split[0]
        return http.local_redirect(
            direction,
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/contacto'], type='http', auth='public', website=True)
    def contact_page(self):
        return http.local_redirect(
            '/page/contactus',
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/pedido-rapido'], type='http', auth='public', website=True)
    def cart_page(self):
        return http.local_redirect(
            '/shop/cart',
            dict(http.request.httprequest.args),
            True,
            code='301'
        )

    @http.route(['/es/blog/<path:path>'], type='http', auth='public', website=True)
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

# import ipdb;
# ipdb.set_trace()