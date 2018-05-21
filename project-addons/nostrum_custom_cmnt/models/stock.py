# -*- coding: utf-8 -*-
# Copyright 2014 Pedro M. Baeza - Tecnativa <pedro.baeza@tecnativa.com>
# Copyright 2015 Antonio Espinosa - Tecnativa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.multi
    def sale_lines_values(self, sale_lines):
        res = super(StockPackOperation, self).sale_lines_values(sale_lines)
        sale_line = sale_lines[:1]
        sale_tax = sale_line.tax_id
        res.update({
            'sale_tax_description': ', '.join(map(lambda x: (
                x.name), sale_tax)),
        })
        return res
