# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com
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


from openerp import models


class StockMove(models.Model):
    _inherit = "stock.move"

    # TODO MIGRATE BIEN, ESTE METODO NO EXISTE, PROPAGAR DESDE EL MOVIMIENTO A
    # LA LÍNEA
    # def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type,
    # context=None):
    #     res = super(StockMove, self)._get_invoice_line_vals(cr, uid, move, p
    # Partner, inv_type, context=context)
    #     qty = 0
    #     amount = 0
    #     for quant in move.quant_ids:
    #         amount = amount + quant.inventory_value
    #         qty = qty + quant.qty
    #     if qty > 0:
    #         purchase_price = amount / qty
    #         res['purchase_price'] = purchase_price
    #     return res
