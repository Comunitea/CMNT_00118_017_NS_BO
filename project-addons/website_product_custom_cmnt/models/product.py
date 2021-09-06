# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    udi_code = fields.Char(string='UDI code')
    