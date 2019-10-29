# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __odoo__.py file in root directory
##############################################################################
from odoo import fields, models, api, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

 
    is_component = fields.Boolean('Es componente', readonly=False)
