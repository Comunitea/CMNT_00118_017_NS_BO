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


from openerp import models, fields, api


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    transportista = fields.Char(string="Transportista",
                                compute='_get_datos_albaran')
    web_transportista = fields.Char(string="Web Transportista",
                                    compute='_get_datos_albaran')
    num_seguimiento = fields.Char(string="Num seguimiento",
                                  compute='_get_datos_albaran')

    @api.multi
    def _get_datos_albaran(self):
        for record in self:
            transportista = ''
            num_seguimiento = ''
            web_transportista = ''
            for sale in record.sale_ids:
                for alb in sale.picking_ids:
                    num_seguimiento = alb.carrier_tracking_ref
                    if alb.carrier_id:
                        transportista = alb.carrier_id.name
                        web_transportista = alb.carrier_id.web
                        if 'Sending' in transportista:
                            num_seguimiento = alb.sending_expedicion
            record.transportista = transportista
            record.num_seguimiento = num_seguimiento
            record.web_transportista = web_transportista
