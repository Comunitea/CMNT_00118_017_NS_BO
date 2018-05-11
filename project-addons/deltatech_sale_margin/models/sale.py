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


from odoo import models, api, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # La definición del campo purchase price se mueve a sale_margin_percentage
    # aunuqe ya está declarada en sale_margin

    # Comentado postmigración por no ser necesario al tener la restrición
    # de abajo
    # def product_id_change(self):
    #     res = super(SaleOrderLine, self).product_id_change()
    #     if not res.get('warning', False):
    #         if self.price_unit and self.purchase_price:
    #             if self.price_unit < self.purchase_price:
    #                 warning = {
    #                     'title': _('Price Error!'),
    #                     'message': _('You can not sell below the purchase \
    #                                  price.')
    #                 }
    #                 res['warning'] = warning
    #     return res

    # @api.one
    # @api.constrains('price_unit', 'purchase_price')
    # def _check_seats_limit(self):
    #     if not self.env['res.users'].\
    #         has_group('deltatech_sale_margin.\
    #                    group_sale_below_purchase_price'):
    #         if self.price_unit < self.purchase_price:
    #             raise Warning(_('You can not sell below the \
    #                              purchase price.'))

    # Quito herencia write, porque estaba escribiendo el precio de compra
    # cuando el precio de venta es 0, esto es peligroso

    # POST MIGRATION: Sustituyo el onchange de arriba y el contraint de abajo
    @api.onchange('product_id', 'price_unit', 'purchase_price')
    def priuce_and_cost_id_change(self):
        res = {}
        for line in self:
            if line.price_unit < line.purchase_price:
                warning = {
                    'title': _('Price Error!'),
                    'message': _('You can not sell below the purchase \
                                 price.')
                }
                res['warning'] = warning
        return res

    # POST MIGRATION: mÉTODO PARA PASAR EL PUCHASE_PRICE A LA FACTURA
    # SUSTITUYE AL QUE HABÍA PARA PASARLA SOBRE STOCK MOVE
    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update(purchase_price=self.purchase_price)
        return res
