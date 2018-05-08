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
from odoo import api, models, fields, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime
import sys
from ..mrw.picking import *
reload(sys)
sys.setdefaultencoding('iso-8859-1')


class StockPicking(models.Model):
    # Overloaded stock_picking to manage carriers :
    _inherit = 'stock.picking'

    @api.multi
    def _get_delivery_address(self):
        res = {}
        for pick in self.browse():
            direccion = pick.partner_id.street
            codigo_postal = pick.partner_id.zip
            poblacion = pick.partner_id.city
            provincia = pick.partner_id.state_id.name
            pais = pick.partner_id.country_id.name
            telefono = pick.partner_id.phone
            contacto = pick.partner_id.name.encode("UTF-8")

            pick.delivery_poblacion = poblacion
            pick.delivery_provincia = provincia
            pick.delivery_direccion = direccion
            pick.delivery_pais = pais
            pick.delivery_telefono = telefono
            if pick.partner_id.country_id:
                    if pick.partner_id.country_id.code == 'PT' and \
                            codigo_postal:
                        pick.delivery_contacto = contacto
        return res

    observaciones = fields.Text(string='Observaciones',
                                help="Estas observaciones apareceran en la \
                                      etiqueta de envio")
    mrw_codigo_servicio = fields.Selection([
        ('0000', 'Urgente 10'),
        ('0005', 'Urgente Hoy'),
        ('0010', 'Promociones'),
        ('0100', 'Urgente 12'),
        ('0110', 'Urgente 14'),
        ('0120', 'Urgente 22'),
        ('0200', 'Urgente 19'),
        ('0205', 'Urgente 19 Expedicion'),
        ('0210', 'Urgente 19 Mas 40 Kilos'),
        ('0220', 'Urgente 19 Portugal'),
        ('0230', 'Bag 19'),
        ('0235', 'Bag 14'),
        ('0300', 'Economico'),
        ('0310', 'Economico Mas 40 Kilos'),
        ('0350', 'Economico Interinsular'),
        ('0400', 'Express Documentos'),
        ('0450', 'Express 2 Kilos'),
        ('0480', 'Caja Express 3 Kilos'),
        ('0490', 'Documentos 14'),
        ('0800', 'Ecommerce'),
        ('0810', 'Ecommerce Canje')], string='Código Servicio', default='0300')
    mrw_fecha_recogida = fields.Datetime(string='Fecha recogida',
                                         help='Fecha de recogida, \
                                         por defecto pasara la fecha actual')
    mrw_reembolso = fields.Selection([
        ('N', 'Sin reembolso'),
        ('O', 'Con reembolso comisión en origen'),
        ('D', 'Con reembolso comisión en destino')],
        string='Reembolso', default='N',
        help='Indica el parametro a pasar a mrw segun el modo de pago del \
        pedido')
    mrw_importe_reembolso = fields.\
        Float(string='Importe Reembolso',
              digits_compute=dp.get_precision('Totales RC'),
              help='Importe del pedido cuando el modo de pago es \
                    contra-reembolso')
    delivery_direccion = fields.Char(compute='_get_delivery_address',
                                     string='Direccion Entrega',
                                     help='Direccion del Cliente de Entrega')
    delivery_zip = fields.Char(compute='_get_delivery_address',
                               string='Codigo Postal Entrega',
                               help='Codigo Postal del Cliente de Entrega')
    delivery_poblacion = fields.Char(compute='_get_delivery_address',
                                     string='Población Entrega',
                                     help='Población del Cliente de Entrega')
    delivery_provincia = fields.Char(compute='_get_delivery_address',
                                     string='Provincia Entrega',
                                     help='Provincia del Cliente de Entrega')
    delivery_pais = fields.Char(compute='_get_delivery_address',
                                string='Pais Entrega',
                                help='Pais del Cliente de Entrega')
    delivery_telefono = fields.Char(compute='_get_delivery_address',
                                    string='Telefono Entrega',
                                    help='Telefono del Cliente de Entrega')
    delivery_contacto = fields.Char(compute='_get_delivery_address',
                                    string='Contacto Entrega',
                                    help='Persona de contacto del \
                                          Cliente de Entrega')
    carrier_error = fields.Char(string='Resultado solicitud',
                                readonly=True, size=255)
    mrw_enfranquicia = fields.Boolean(string='Entrega en Franquicia')
    mrw_entregasabado = fields.Selection([('N', 'No'),
                                          ('S', 'Si')],
                                         string='Entrega en Sabado',
                                         default='N')

    @api.model
    def create(self, vals):
        # Actualiza los datos de MRW al crear el albaran
        if 'origin' in vals:
            carrier_obj = self.env['delivery.carrier']
            sale_line_obj = self.env['sale.order.line']
            mrw_carrier_id = False
            mrw_carrier_obj = carrier_obj.search([('name', '=', 'MRW')],
                                                 limit=1)

            if mrw_carrier_obj:
                mrw_carrier_id = mrw_carrier_obj.id
            domain = [('order_id.name', '=', vals['origin']),
                      ('product_id.name', '=', 'Shipping'),
                      ('name', 'ilike', 'MRW')]
            sale_line_objs = sale_line_obj.search(domain)
            for sale_line in sale_line_objs:
                mrw_entregasabado = 'N'
                mrw_reembolso = 'N'
                mrw_importe_reembolso = ''
                mrw_codigo_servicio = '0300'

                mrw_shipping_desc = sale_line.name.upper()
                if ((mrw_shipping_desc.find('SABADO') == -1) &
                        (mrw_shipping_desc.find('SATURDAY') == -1)):
                    mrw_entregasabado = 'N'
                else:
                    mrw_entregasabado = 'S'

                if sale_line.order_id.payment_mode_id.name == \
                        'CONTRA REEMBOLSO':
                    mrw_reembolso = 'O'
                    mrw_importe_reembolso = str(sale_line.order_id.
                                                amount_total)

                if mrw_carrier_id:
                    vals['carrier_id'] = mrw_carrier_id
                vals['mrw_reembolso'] = mrw_reembolso
                vals['mrw_importe_reembolso'] = mrw_importe_reembolso
                vals['mrw_codigo_servicio'] = mrw_codigo_servicio
                vals['mrw_entregasabado'] = mrw_entregasabado
        return super(StockPicking, self).create(vals)

    @api.model
    def send_mail_tracking(self):
        email_template_obj = self.env['email.template']
        domain = [('name', '=', 'Enviar Aviso Tracking (MRW)')]
        template_obj = email_template_obj.search(domain, limit=1)
        print 'ENVI POR EMAIL'
        if template_obj:
            for picking in self:
                if picking.carrier_tracking_ref:
                    values = email_template_obj.\
                        generate_email(template_obj.id, picking.sale_id.id)
                    values['res_id'] = picking.sale_id.id
                    values['partner_ids'] = \
                        [picking.sale_id.partner_invoice_id.id]
                    values['notified_partner_ids'] = \
                        [picking.sale_id.partner_invoice_id.id]
                    values['email_to'] = \
                        picking.sale_id.partner_invoice_id.email
                    values['notification'] = True
                    mail_mail_obj = self.pool.get('mail.mail')
                    msg_id = mail_mail_obj.create(values)
                    if msg_id:
                        msg_id.send()
        return True

    @api.multi
    def button_mrwenvio(self):
        self.ensure_one()
        print 'Comienzo creacion etiqueta MRW'
        carrier_obj = self.env['delivery.carrier']
        deliv = self
        # Recuperamos los datos de transporte de pedidos
        carrier_obj = self.env['delivery.carrier']
        reference = False
        mrw_carrier_id = False
        mrw_carrier_obj = carrier_obj.search([('name', '=', 'MRW')], limit=1)
        if mrw_carrier_obj > 0:
            mrw_carrier_id = mrw_carrier_obj.id
        if not mrw_carrier_id:
            raise UserError(
                _('Error Envio MRW'),
                _('No se encuentra tranportista MRW'))

        if mrw_carrier_id != deliv.carrier_id.id:
            raise UserError(
                _('Error Envio MRW'),
                _('Este albaran no tiene como transportista a MRW'))

        if deliv.carrier_tracking_ref:
            mess_id = self.env['indaws_wizard.message'].\
                create({
                    'text': 'El pedido tiene ya generado un numero de tracking'
                })
        return {
            'name': _("Information"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'indaws_wizard.message',
            'res_id': mess_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

        mrw = True
        if mrw:
            mrw_conf_obj = self.env['indaws_mrw.configuracion']
            mrw_conf_objs = mrw_conf_obj.search([('active', '=', True)])

            if not mrw_conf_objs:
                raise UserError(
                    _('Error Envio MRW'),
                    _('No están configurados los datos de conexión para MRW'))

            else:
                mrw_conf = mrw_conf_objs[0]
                username = mrw_conf.username or ''
                password = mrw_conf.password or ''
                franchise = mrw_conf.franchise or ''
                subscriber = mrw_conf.subscriber or ''
                department = mrw_conf.department or ''
                debug = mrw_conf.debug
                fecha_c = ''

                # if deliv.weight:
                #     peso = int(math.ceil(deliv.weight))
                # else:
                #     peso = ''

                if deliv.mrw_fecha_recogida:
                    fecha_d = datetime.strptime(deliv.mrw_fecha_recogida,
                                                '%Y-%m-%d %H:%M:%S')
                    fecha_c = fecha_d.strftime('%d/%m/%Y')
                else:
                    fecha_d = datetime.strptime(fields.datetime.now(),
                                                '%Y-%m-%d %H:%M:%S')
                    fecha_c = fecha_d.strftime('%d/%m/%Y')

                if deliv.number_of_packages == 0:
                    bultos = 1
                else:
                    bultos = deliv.number_of_packages

                if deliv.mrw_enfranquicia:
                    mrw_enfranquicia = 'E'
                else:
                    mrw_enfranquicia = 'N'

                # mrw_entregasabado = deliv.mrw_entregasabado

                ref = 'PEDIDO: ' + deliv.origin

                importe = str(deliv.mrw_importe_reembolso).replace(".", ",")
                print 'Empiezo a contruir API de Solicitud de Envio'
                # API de Solicitud de Envio
                picking_api = Picking(username, password, franchise,
                                      subscriber, department, debug)
                data = {}
                data['via'] = deliv.delivery_direccion and \
                    unquote_plus(deliv.delivery_direccion.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['codigo_postal'] = deliv.delivery_zip or ''
                data['poblacion'] = deliv.delivery_poblacion and \
                    unquote_plus(deliv.delivery_poblacion.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['provincia'] = deliv.delivery_provincia and \
                    unquote_plus(deliv.delivery_provincia.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['nif'] = deliv.partner_id.vat or ''
                data['nombre'] = deliv.partner_id.name and \
                    unquote_plus(deliv.partner_id.name.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['telefono'] = deliv.delivery_telefono or ''
                data['contacto'] = deliv.delivery_contacto and \
                    unquote_plus(deliv.delivery_contacto.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['atencion_de'] = deliv.delivery_contacto and \
                    unquote_plus(deliv.delivery_contacto.
                                 encode('utf-8', 'xmlcharrefreplace')) or ''
                data['observaciones'] = deliv.observaciones or ''
                data['fecha'] = fecha_c or ''
                data['referencia'] = ref
                data['codigo_servicio'] = deliv.mrw_codigo_servicio
                data['bultos'] = bultos or ''
                data['peso'] = 1  # lo pasamos siempre a 1Kg
                data['reembolso'] = deliv.mrw_reembolso
                data['importe_reembolso'] = importe
                data['entregasabado'] = deliv.mrw_entregasabado
                data['enfranquicia'] = mrw_enfranquicia
                print 'Llamada a API de Solicitud de Envio'
                reference, error = picking_api.create(data)
                url = ''

                if reference:
                    # Actualiza numero de tracking en albaran y pedido
                    deliv.write({'carrier_tracking_ref': reference,
                                 'mrw_fecha_recogida': fecha_d,
                                 'number_of_packages': bultos})
                    # Al actualizar el numero de tracking en pedido,
                    # se envia un correo al cliente
                    if deliv.sale_id:
                        deliv.sale_id.write({'tracking': 'MRW ' + reference})
                    # Email al cliente
                    self.send_mail_tracking()

                    # Obtiene la url para ver la etiqueta
                    if debug:
                        url = 'http://sagec-test.mrw.es/Panel.aspx?Franq=%s\
                               &Ab=%s&Dep=&Pwd=%s&Usr=%s&NumEnv=%s' % \
                            (franchise, subscriber, password, username,
                             reference)
                    else:
                        url = 'http://sagec.mrw.es/Panel.aspx?Franq=%s&Ab=%s\
                               &Dep=&Pwd=%s&Usr=%s&NumEnv=%s' % \
                            (franchise, subscriber, password, username,
                             reference)
                if error:
                    self.write({'carrier_error': error})
                    mess_id = self.env['indaws_wizard.message'].\
                        create({'text': error})

        if reference:
            return {
                'name': 'Go to website',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url
            }
        else:
            return {
                'name': _("Information"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'indaws_wizard.message',
                'res_id': mess_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
            }

    @api.multi
    def button_mrwetiqueta(self):
        self.ensure_one()
        deliv = self[0]
        mrw_conf_obj = self.env['indaws_mrw.configuracion']
        mrw_conf_objs = mrw_conf_obj.search([('active', '=', True)])

        if mrw_conf_objs:
            mrw_conf = mrw_conf_objs[0]
            username = mrw_conf.username or ''
            password = mrw_conf.password or ''
            franchise = mrw_conf.franchise or ''
            subscriber = mrw_conf.subscriber or ''
            debug = mrw_conf.debug
            reference = deliv.carrier_tracking_ref

            if debug:
                url = 'http://sagec-test.mrw.es/Panel.aspx?Franq=%s&Ab=%s\
                       &Dep=&Pwd=%s&Usr=%s&NumEnv=%s' %\
                    (franchise, subscriber, password, username, reference)
            else:
                url = 'http://sagec.mrw.es/Panel.aspx?Franq=%s&Ab=%s&Dep=&\
                       Pwd=%s&Usr=%s&NumEnv=%s' %\
                    (franchise, subscriber, password, username, reference)

        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url
        }
