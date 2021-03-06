# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    _inherits = {'product.product': 'product_id'}
    _description = "Carrier"
    _order = 'sequence, id'

    weight_base_max = fields.Float('Máximo Peso Base', required=False, help="Peso Maximo a partir del que \
                                    empiezan los rangos por tramos de sobrepeso. Ej: 15Kg.")
    weight_range = fields.Float('Factor Tramo Sobreeso', required=False, help="Factor de rango a aplicar por tramos de \
                                 peso a partir del peso maximo base. Ej: 5, aplica un sobrepeso cada 5kg a partir del \
                                 peso maximo base")
    weight_total_max = fields.Float('Máximo Peso Admisible', required=False, help="Peso Maximo a partir del cual \
                                     ya no se envía la mercancía. Ej: 20Kg. Si se deja a cero no se aplicará este \
                                     criterio. Ej: 0Kg.")

    def get_price_from_picking(self, total, weight, volume, quantity):
        """
        Actualiza el precio teniendo en cuenta si hay una segunda condicion en las reglas pero solo se evalua
        si la primera es True sino solo se evalua la primera condicion.
        """
        price = 0.0
        criteria_found = False
        overweight = 0.0

        # overweight is optional. Only evaluate if is present
        if weight and self.weight_base_max and weight > self.weight_base_max:
            overweight = divmod(weight - self.weight_base_max, self.weight_range)[0]

        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity,
                      'overweight': overweight}

        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            # Second condition is optional. Only evaluate if is present and first condition is True
            if test is True and line.max_value_2 and line.max_value_2 > 0:
                test = safe_eval(line.variable_2 + line.operator_2 + str(line.max_value_2), price_dict)
            if test:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
        if not criteria_found:
            raise UserError("El producto elegido en el método de entrega no cumple ninguno de los criterios de los \
                             transportistas de entrega.")

        return price

    @api.multi
    def get_price_available(self, order):
        self.ensure_one()
        # total = 0
        weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line.filtered(
                lambda x: x.is_delivery or x.product_id.type not in ('service', 'digital')):
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_total
            if not line.product_id or line.is_delivery:
                continue
            qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        # total = (order.amount_total or 0.0) - total_delivery
        total = (order.no_digital_products_total or 0.0) - total_delivery

        total = order.currency_id.with_context(date=order.date_order).compute(total, order.company_id.currency_id)

        return self.get_price_from_picking(total, weight, volume, quantity)
