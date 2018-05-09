# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    vendor_ref = fields.Char('Vendor Reference',
                             related='partner_id.vendor_ref')
    customer_ref = fields.Char('Customer Reference',
                               related='partner_id.customer_ref')
    payment_term = fields.Many2one(required=True, readonly=False)
    payment_mode_id = fields.Many2one(required=True)
