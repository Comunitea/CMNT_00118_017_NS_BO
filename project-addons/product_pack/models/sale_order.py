# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __odoo__.py file in root directory
##############################################################################
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        # we unlink pack lines that should not be copied
        sale_copy = super(SaleOrder, self).copy(default)
        pack_copied_lines = sale_copy.order_line.filtered(
            lambda l: l.pack_parent_line_id.order_id.id == self.id)
        pack_copied_lines.unlink()
        return sale_copy
