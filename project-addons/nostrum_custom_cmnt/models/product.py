# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    internal_note = fields.Text('Internal Note')


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.one
    def _get_pricelist_item_name_price(self):
        res = super(PricelistItem, self)._get_pricelist_item_name_price()
        # Show alwais code
        if self.product_id:
            self.name = self.product_id.display_name
        return res
