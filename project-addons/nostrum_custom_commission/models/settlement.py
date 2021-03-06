# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SettlementLine(models.Model):
    _inherit = 'sale.commission.settlement.line'

    invoice = fields.Many2one(store=True)
    partner_id = fields.Many2one('res.partner', 
                                 related='invoice.partner_id', store=True)
    commission = fields.Many2one(store=True)
