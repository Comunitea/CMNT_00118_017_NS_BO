from odoo import tools
from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    price_subtotal = fields.Float(store=True)
    price_subtotal_incl = fields.Float(store=True)

