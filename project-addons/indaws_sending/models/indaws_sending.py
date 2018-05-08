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

from odoo import fields, models


class IndawsSendingProduct(models.Model):
    _name = "indaws_sending.product"

    name = fields.Char('Denominación', size=60)
    codigo = fields.Char('Codigo', size=2)
    sigla = fields.Char('Sigla', size=30)
    cod_porte_pagado = fields.Char('Codigo Portes Pagados', size=30)
    cod_porte_debido = fields.Char('Codigo Portes Debidos', size=30)


class IndawsSendingPickingBultos(models.Model):
    _name = "indaws_sending.picking_bultos"

    picking_id = fields.Many2one('stock.picking', 'Albaran')
    numbulto = fields.Integer('Numero Bulto')
    referencia = fields.Char('Referencia', size=30)
    descripcion = fields.Char('Descripcion', size=30)
    observaciones = fields.Char('Observaciones', size=50)
    kilos = fields.Float('Kilos')
    volumen = fields.Float('Volumen')
    alto = fields.Float('Alto')
    largo = fields.Float('Largo')
    ancho = fields.Float('Ancho')
    codbarras = fields.Char('Codigo Barras')
