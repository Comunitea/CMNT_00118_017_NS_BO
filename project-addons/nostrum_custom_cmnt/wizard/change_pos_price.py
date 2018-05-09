# -*- coding: utf-8 -*-
# © 2017 Comunitea Servicios Tecnológicos S.L. (http://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ChangePosPrice(models.TransientModel):
    _name = 'change.pos.price'
    _description = 'Change Price Unit'

    new_price = fields.Float('New Price Unit',
                             digits=dp.get_precision('Product Price'))

    @api.multi
    def apply(self):
        self.ensure_one()
        active_id = self._context.get('active_id')
        pos_line = self.env['pos.order.line'].browse(active_id)
        pos_line.write({'price_unit': self.new_price})
        for paid in pos_line.order_id.statement_ids:
            if paid.amount < 0:
                paid.unlink()
            else:
                paid.write({'amount': pos_line.order_id.amount_total})
        return
