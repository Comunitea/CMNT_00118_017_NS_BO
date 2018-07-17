# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a pos order.
        """
        res = super(PosOrder, self)._prepare_invoice()
        res.update(payment_mode_id=self.partner_id.customer_payment_mode_id.id)
        return res
