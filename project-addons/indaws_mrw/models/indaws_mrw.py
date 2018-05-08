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

from odoo import models, fields, api
from ..mrw.api import API


class IndawsMrwConfiguracion(models.Model):
    _name = "indaws_mrw.configuracion"

    username = fields.Char('Usuario', required=True, size=64)
    password = fields.Char('Contraseña', required=True, size=64)
    franchise = fields.Char('Franquicia', required=True, size=64)
    subscriber = fields.Char('Abonado', required=True, size=64)
    department = fields.Char('Departamento', size=64)
    status = fields.Char('Estado conexión', readonly=True, size=255)
    debug = fields.Boolean('Test', default=True)
    active = fields.Boolean('Active', default=True)

    @api.multi
    def test_connection(self):
        obj = self[0]
        username = obj.username or False
        password = obj.password or False
        franchise = obj.franchise or False
        subscriber = obj.subscriber or False
        department = obj.department or ''
        debug = obj.debug

        mrw_api = API(username, password, franchise, subscriber, department,
                      debug)
        status = mrw_api.test_connection()
        self.write({'status': status})
        return True
