# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    internal_note = fields.Text('Internal Note')
