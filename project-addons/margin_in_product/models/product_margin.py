from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    margin_percent = fields.Float(compute="_product_margin", string='Margin %',
                                  save=True,
                                  help="It gives profitability by calculating \
                                  the difference between the Price for the \
                                  customers and the cost price.")

    @api.multi
    @api.depends("list_price", "standard_price")
    def _product_margin(self):
        for product in self:
            per = 0
            if product.list_price != 0:
                margin = (product.list_price - product.standard_price)
                per = (margin * 100) / product.list_price
            product.margin_percent = per


class ProductProduct(models.Model):
    _inherit = "product.product"

    margin_percent = fields.Float(compute="_product_margin",
                                  string='Margin %',
                                  save=True,
                                  help="It gives profitability by calculating \
                                  the difference between the Price for the \
                                  customers and the cost price.")

    @api.multi
    @api.depends("lst_price", "standard_price")
    def _product_margin(self):
        for product in self:
            per = 0
            if product.list_price != 0:
                margin = (product.lst_price - product.standard_price)
                per = (margin * 100) / product.lst_price
            product.margin_percent = per
