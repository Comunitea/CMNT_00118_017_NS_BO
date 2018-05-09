# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProductSupplirtinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # COMENTADO YA NO HAY CAMPO PRICELIST_IDS
    # cost = fields.Float('Cost',
    #                     related='pricelist_ids.price', readonly=True)
