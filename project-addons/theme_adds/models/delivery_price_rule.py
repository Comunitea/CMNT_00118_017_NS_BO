# -*- coding: utf-8 -*-
#
# © 2018 Comunitea - Ruben Seijas <ruben@comunitea.com>
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PriceRule(models.Model):
    _inherit = "delivery.price.rule"
    _description = "Delivery Price Rules"
    _order = 'sequence, list_price'

    variable_2 = fields.Selection([('weight', 'Peso'), ('volume', 'Volumen'), ('wv', 'Peso * Volumen'),
                                   ('price', 'Precio'), ('quantity', 'Cantidad')], 'Variable',
                                  required=False, default='weight')
    operator_2 = fields.Selection([('==', '='), ('<=', '<='), ('<', '<'), ('>=', '>='), ('>', '>')], 'Operador',
                                  required=False, default='<=')
    max_value_2 = fields.Float('Maximo Valor', required=False)
    variable_factor = fields.Selection(
        [('weight', 'Peso'), ('volume', 'Volumen'), ('wv', 'Peso * Volumen'), ('price', 'Precio'),
         ('quantity', 'Cantidad'), ('overweight', 'Factor Sobrepeso')], 'Factor Variable', required=True,
        default='weight')

    @api.depends('variable', 'operator', 'max_value', 'variable_2', 'operator_2', 'max_value_2', 'list_base_price',
                 'list_price', 'variable_factor')
    def _get_name(self):
        for rule in self:

            name = 'if %s %s %s' % (rule.variable, rule.operator, rule.max_value)
            if rule.max_value_2 > 0:
                name = '%s and %s %s %s' % (name, rule.variable_2, rule.operator_2, rule.max_value_2)
            name = '%s then' % name

            if rule.list_base_price and not rule.list_price:
                name = '%s fixed price %s' % (name, rule.list_base_price)
            elif rule.list_price and not rule.list_base_price:
                name = '%s %s times %s' % (name, rule.list_price, rule.variable_factor)
            else:
                name = '%s fixed price %s and %s times %s Extra' % (name, rule.list_base_price, rule.list_price,
                                                                    rule.variable_factor)
            rule.name = name

