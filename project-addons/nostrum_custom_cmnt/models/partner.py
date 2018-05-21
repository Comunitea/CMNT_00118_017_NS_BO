# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    valued_picking = fields.Boolean(default=False)
