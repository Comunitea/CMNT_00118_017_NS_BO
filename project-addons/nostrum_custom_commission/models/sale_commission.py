# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api, _


class SaleCommission(models.Model):
    _inherit = 'sale.commission'

    amount_base_type = fields.Selection(
         selection_add=[('min_price', _('Min Price difference'))], 
         default='min_price')