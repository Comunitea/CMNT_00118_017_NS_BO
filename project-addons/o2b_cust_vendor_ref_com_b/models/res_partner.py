# -*- encoding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_ref = fields.Char('Customer Reference')
    vendor_ref = fields.Char('Vendor Reference')
