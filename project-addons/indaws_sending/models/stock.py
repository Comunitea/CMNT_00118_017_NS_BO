# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import sys
from ..sending.service import SendingService
from datetime import datetime
from urllib import unquote_plus
reload(sys)
sys.setdefaultencoding('iso-8859-1')


class StockPicking(models.Model):
    # Overloaded stock_picking to manage carriers :
    _inherit = 'stock.picking'

    def _get_sending(self):
        res = {}
        for pick in self:
            carrier_id = pick.carrier_id.id
            sending_company_id = pick.company_id.sending_carrier_id.id
            picking_type = pick.picking_type_id.code
            slist = ['done', 'waiting', 'confirmed', 'assigned',
                     'partially_available']
            if carrier_id == sending_company_id and pick.state in slist and \
                    picking_type == 'outgoing':
                pick.sending = True
            else:
                pick.sending = False

        return res

    sending = fields.Boolean(compute='_get_sending',
                             string='Campos visibles Sending')
    sending_fecha = fields.Datetime('Fecha Envio')
    sending_numbultos = fields.Integer('Numero Bultos')
    sending_kilos = fields.Integer('Kilos', digits=(16, 2))
    sending_volumen = fields.Float('Volumen', digits=(16, 2))
    sending_alto = fields.Float('Alto', digits=(16, 2))
    sending_largo = fields.Float('Largo', digits=(16, 2))
    sending_ancho = fields.Float('Ancho', digits=(16, 2))
    sending_producto = fields.Many2one('indaws_sending.product', 'Producto')
    sending_portes = fields.Selection([('P', 'Pagado'),
                                       ('D', 'Debido')], 'Portes',
                                      default='P')
    sending_reembolso = fields.Float('Reembolso', digits=(16, 2))
    sending_entrsabado = fields.Selection([('S', 'Si'),
                                           ('N', 'No')],
                                          'Entrega Sábado', default='N')
    sending_retorno = fields.Selection([('N', 'No'),
                                        ('S', 'Si')],
                                       'Retorno', default='N')
    sending_seguro = fields.Float('Seguro', digits=(16, 2))
    sending_numenviovuelta = fields.Integer('Numero Envio Vuelta')
    sending_observaciones = fields.Text('Observaciones')
    sending_expedicion = fields.Char('Numero de Expedicion', size=30)
    sending_error = fields.Char('Codigo Error', size=20)
    sending_mensaje_error = fields.Text('Mensaje Error')
    sending_codunico = fields.Char('Codunico', size=240)
    sending_codunico = fields.Char('Codunico', size=240)
    sending_bultos_ids = fields.One2many('indaws_sending.picking_bultos',
                                         'picking_id', 'Detalle Bultos')
    url_etiqueta = fields.Char('Descargar Etiqueta', size=240)

    def get_data(self):
        for picking in self:
            company = picking.company_id

            xml = ''

            if picking.sending_fecha:
                fecha = datetime.strptime(picking.sending_fecha,
                                          '%Y-%m-%d %H:%M:%S')
            else:
                fecha = datetime.strptime(fields.datetime.now(),
                                          '%Y-%m-%d %H:%M:%S')
            fecha_formateada = fecha.strftime('%d/%m/%Y')

            if picking.partner_id.mobile:
                telefono = picking.partner_id.mobile
            elif picking.partner_id.phone:
                telefono = picking.partner_id.phone

            if picking.sending_observaciones:
                observaciones =\
                    unquote_plus(picking.
                                 sending_observaciones('utf-8',
                                                       'xmlcharrefreplace'))
            else:
                observaciones = ''
            if picking.sending_entrsabado is False:
                picking.sending_entrsabado == 'N'
            elif picking.sending_entrsabado == 'S':
                picking.sending_entrsabado == 'S'

            if picking.sending_portes == 'D':
                picking.sending_portes == 'D'

            if picking.sending_retorno == 'S':
                picking.sending_retorno == 'S'

            if picking.sending_reembolso > 0:
                picking.sending_reembolso = str(picking.sending_reembolso)
            else:
                picking.sending_reembolso = ''

            xml += '<Expediciones>'
            xml += '<Expedicion>'
            xml += '<Fecha>' + str(fecha_formateada) + '</Fecha>'
            # datos remitente
            xml += '<ClienteRemitente>' + company.sending_center + \
                '</ClienteRemitente>'
            xml += '<NombreRemitente>' + company.name + \
                '</NombreRemitente>'
            xml += '<DireccionRemitente>' + company.street + \
                '</DireccionRemitente>'
            xml += '<PaisRemitente>034</PaisRemitente>'
            xml += '<CodigoPostalRemitente>' + company.zip + \
                '</CodigoPostalRemitente>'
            xml += '<PoblacionRemitente>' + company.city + \
                '</PoblacionRemitente>'

            # datos destinatario
            xml += '<NombreDestinatario>' + picking.partner_id.name + \
                '</NombreDestinatario>'
            xml += '<DireccionDestinatario>' + picking.partner_id.street + \
                '</DireccionDestinatario>'
            xml += '<PaisDestinatario>034</PaisDestinatario>'
            xml += '<CodigoPostalDestinatario>' + picking.partner_id.zip + \
                '</CodigoPostalDestinatario>'
            xml += '<PoblacionDestinatario>' + picking.partner_id.city + ' \
                </PoblacionDestinatario>'
            xml += '<PersonaContactoDestinatario>' + picking.partner_id.name \
                + '</PersonaContactoDestinatario>'
            xml += '<TelefonoContactoDestinatario>' + telefono + \
                '</TelefonoContactoDestinatario>'
            xml += '<EnviarMail></EnviarMail>'
            xml += '<MailDestinatario>' + picking.partner_id.email + \
                '</MailDestinatario>'

            # datos envio
            num_ref = picking.name
            if num_ref:
                num_ref = picking.name.replace("\\", "")
                num_ref = num_ref.replace("WHOUT", "")
            xml += '<ProductoServicio>01</ProductoServicio>'
            xml += '<Observaciones1>' + observaciones + '</Observaciones1>'
            xml += '<Kilos>' + str(int(picking.sending_kilos)) + '</Kilos>'
            xml += '<Volumen>' + str(picking.sending_volumen) + '</Volumen>'
            xml += '<ReferenciaCl i ente>' + picking.name + \
                '</ReferenciaCliente>'
            xml += '<TipoPortes>' + picking.sending_portes + '</TipoPortes>'
            xml += '<EntregaSabado>' + picking.sending_entrsabado + \
                '</EntregaSabado>'
            xml += '<Retorno>' + picking.sending_retorno + '</Retorno>'
            xml += '<Bultos>' + str(picking.sending_numbultos) + '</Bultos>'
            xml += '</Expedicion></Expediciones>'

        return xml

    @api.multi
    def button_sending_etiqueta(self):
        self.ensure_one()
        picking = self
        self.check_data(picking)

        company = picking.company_id
        username = company.sending_username or False
        center = company.sending_center or False
        password = company.sending_password or False

        sending_api = SendingService(username, password)

        xml = self.get_data()

        response = sending_api.grabar_envio(xml, center)

        sending_mensaje_error = ''
        sending_expedicion = ''
        codigo = ''
        expedicion = ''

        if len(response.split()) == 2:
            codigo, expedicion = response.split()
            if codigo == 'OK':
                sending_expedicion = expedicion
            else:
                sending_mensaje_error = codigo + ': ' + expedicion
        else:
            devuelve = response.split()
            expedicion = devuelve[-1]
            sending_mensaje_error = ' '.join(devuelve[:-1])
            sending_expedicion = expedicion

        picking.write({'sending_expedicion': sending_expedicion,
                       'sending_mensaje_error': sending_mensaje_error})

        # conseguir PDF
        response = sending_api.conseguir_pdf(sending_expedicion, center)

        response = "http://" + response
        picking.write({'url_etiqueta': response})

    def destino(self):
        destino = {
            '010': 'VITORIA 010',
            '020': 'ALBACETE 020',
            '030': 'ALICANTE 030',
            '040': 'ALMERIA 040',
            '061': 'MERIDA 061',
            '070': 'PALMA DE MALLORCA 070',
            '072': 'MENORCA 072',
            '080': 'BARCELONA 080',
            '090': 'BURGOS 090',
            '100': 'CACERES 100',
            '111': 'JEREZ DE LA FRONTERA 111',
            '112': 'ALGECIRAS 112',
            '120': 'CASTELLON 120',
            '130': 'CIUDAD REAL 130',
            '140': 'CORDOBA 140',
            '150': 'LA CORUÑA 150',
            '151': 'SANTIAGO DE COMPOSTELA 151',
            '160': 'CUENCA 160',
            '170': 'GERONA 170',
            '180': 'GRANADA 180',
            '200': 'SAN SEBASTIAN 200',
            '210': 'HUELVA 210',
            '220': 'HUESCA 220',
            '230': 'JAEN 230',
            '240': 'LEON 240',
            '250': 'LERIDA 250',
            '260': 'LOGROÑO 260',
            '270': 'LUGO 270',
            '280': 'MADRID 280',
            '281': 'COSLADA 281',
            '290': 'MALAGA 290',
            '300': 'MURCIA 300',
            '310': 'PAMPLONA 310',
            '320': 'ORENSE 320',
            '330': 'OVIEDO 330',
            '340': 'PALENCIA 340',
            '350': 'LAS PALMAS 350',
            '361': 'VIGO 361',
            '380': 'TENERIFE 380',
            '390': 'SANTANDER 390',
            '400': 'SEGOVIA 400',
            '410': 'SEVILLA 410',
            '420': 'SORIA 420',
            '430': 'TARRAGONA 430',
            '450': 'TOLEDO 450',
            '460': 'VALENCIA 460',
            '470': 'VALLADOLID 470',
            '480': 'BILBAO 480',
            '491': 'ZAMORA 491',
            '500': 'ZARAGOZA 500',
        }
        return destino

    def create(self, vals):
        # Actualiza los datos de sending al crear el albaran
        if 'origin' in vals:
            carrier_obj = self.env['delivery.carrier']
            sale_line_obj = self.env['sale.order.line']
            sending_carrier_id = False
            sending_carrier_objs = carrier_obj.\
                search([('name', '=', 'sending')], limit=1)

        if sending_carrier_objs:
            sending_carrier_id = sending_carrier_objs[0].id
            domain = [('order_id.name', '=', vals['origin']),
                      ('product_id.name', '=', 'Shipping'),
                      ('name', 'ilike', 'Sending')]
            sale_line_objs = sale_line_obj.search(domain)
            for sale_line in sale_line_objs:
                if sending_carrier_id:
                    vals['carrier_id'] = sending_carrier_id

                    if sale_line.order_id.payment_mode_id.name == \
                            'CONTRA REEMBOLSO':
                        vals['sending_reembolso'] = \
                            str(sale_line.order_id.amount_total)

                prod = False
                d1 = [('id', '=', sale_line.id), ('name', 'ilike', '24H')]
                sale_line_ids24 = sale_line_obj.search(d1)
                if len(sale_line_ids24) > 0:
                    prod = 'PAQ24'
                    print 'encontrato PAQ72 1'

                d2 = [('id', '=', sale_line.id),
                      ('name', 'ilike', '24H a 72H')]
                sale_line_ids72 = sale_line_obj.search(d2)
                if len(sale_line_ids72) > 0:
                    prod = 'PAQ72'
                    print 'encontrato PAQ72 1'

                d3 = [('id', '=', sale_line.id),
                      ('name', 'ilike', 'max. 72H')]
                sale_line_ids72 = sale_line_obj.search(d3)
                if len(sale_line_ids72) > 0:
                    prod = 'PAQ72'
                    print 'encontrato PAQ72 2'

                d4 = [('id', '=', sale_line.id),
                      ('name', 'ilike', 'max. 72H')]
                sale_line_ids48 = sale_line_obj.search(d4)
                if len(sale_line_ids48) > 0:
                    prod = 'PAQ48'
                    print 'encontrato PAQ48 1'
                d5 = [('id', '=', sale_line.id),
                      ('name', 'ilike', '24H-48H')]
                sale_line_ids48 = sale_line_obj.search(d5)
                if len(sale_line_ids48) > 0:
                    prod = 'PAQ48'
                    print 'encontrato PAQ48 3'
                d6 = [('id', '=', sale_line.id),
                      ('name', 'ilike', 'max. 48H')]
                sale_line_ids48 = sale_line_obj.search(d6)
                if len(sale_line_ids48) > 0:
                    prod = 'PAQ48'
                    print 'encontrato PAQ48 2'

                d7 = [('id', '=', sale_line.id),
                      ('name', 'ilike', 'Canarias aereo')]
                sale_line_idsae = sale_line_obj.search(d7)
                if len(sale_line_idsae) > 0:
                    prod = 'CANA'
                    print 'encontrato  1'
                if prod:
                    try:
                        prod_id = self.env.ref('indaws_sending')
                    except ValueError:
                        prod_id = False
                    vals['sending_producto'] = prod_id.id

        return super(StockPicking, self).create(vals)

    @api.model
    def check_data(self, picking):
        #  raise ValidationError(picking.partner_id.name)
        if picking.sending_numbultos == 0:
            raise ValidationError("Debes rellenar el campo 'Numero Bultos'")
            return {}
        if picking.sending_kilos == 0:
            raise ValidationError("Debes rellenar el campo 'Kilos'")
            return {}
        if picking.partner_id.name == '' or picking.partner_id.name is False:
            raise ValidationError("Debes rellenar el campo 'Nombre' del \
                                  cliente")
            return {}
        if picking.partner_id.street == '' or \
                picking.partner_id.street is False:
            raise ValidationError("Debes rellenar el campo 'Calle' del \
                                  cliente")
            return {}
        if picking.partner_id.city == '' or picking.partner_id.city is False:
            raise ValidationError("Debes rellenar el campo 'Ciudad' del \
                                  cliente")
            return {}
        if (picking.partner_id.mobile == '' or
                picking.partner_id.mobile is False):
            if (picking.partner_id.phone == '' or
                    picking.partner_id.phone is False):
                raise ValidationError("Debes rellenar el campo \
                                      'Telefono/Movil' del cliente")
                return {}
        if picking.partner_id.email == '' or picking.partner_id.email is False:
            raise ValidationError("Debes rellenar el campo 'Email' del \
                                   cliente")
            return {}
        if picking.partner_id.zip == '' or picking.partner_id.zip is False:
            raise ValidationError("Debes rellenar el campo 'Codigo Postal' \
                                   del cliente")
            return {}
        return True
