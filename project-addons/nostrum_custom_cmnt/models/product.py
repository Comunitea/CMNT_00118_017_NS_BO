# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    internal_note = fields.Text('Internal Note')

    @api.multi
    def _get_sales_info(self):
        for tmp in self:
            last_year_sales = sum(
                [x.last_year_sales for x in tmp.product_variant_ids])
            
            sum_qty = sum(
                [x.last_year_unit_sales for x in tmp.product_variant_ids])
            
            units_by_month = sum_qty / 12
            stock_months = tmp.qty_available / (units_by_month or 1.0)

            tmp.last_year_sales = last_year_sales
            tmp.average_month_sales = last_year_sales / 12.0
            tmp.last_year_unit_sales = sum_qty
            tmp.remaining_stock_days = stock_months * 30
    
    @api.multi
    def _purchase_count(self):
        for tmp in self:
            tmp.purchase_count = \
                sum([p.purchase_count for p in tmp.product_variant_ids])

    last_year_sales = fields.Integer(
        'Las year sales', compute='_get_sales_info')
    average_month_sales = fields.Float(
        'Average month sales', compute='_get_sales_info')
    last_year_unit_sales = fields.Float(
        'Last year unit sales', compute='_get_sales_info')
    remaining_stock_days = fields.Float(
        'Remainig stock days', compute='_get_sales_info')
    
    purchase_count = fields.Integer(compute='_purchase_count', 
        string='# Purchases')
    
    @api.multi
    def action_view_purchases(self):
        self.ensure_one()
        action = self.env.ref('purchase.action_purchase_line_product_tree')
        product_ids = self.with_context(active_test=False).product_variant_ids.ids

        domain = [('product_id', 'in', product_ids)]
        lines = self.env['purchase.order.line'].search(domain)

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            # 'context': "{'default_product_id': " + str(product_ids[0]) + "}",
            'res_model': action.res_model,
            'domain': [('id', '=', lines.ids)],
        }
    
    # @api.multi
    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)
    #     if vals.get('image', False):
    #         for template in self:
    #             if len(template.product_variant_ids) == 1:
    #                 template.product_variant_ids.write(
    #                     {'image': vals['image']})
    #     return res

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _get_sales_info(self):
        for product in self:
            now = datetime.now()
            last_year = datetime.now() - relativedelta(years=1)

            now_str = now.strftime('%Y-%m-%d')
            last_year_str = last_year.strftime('%Y-%m-%d')

            # BUSCAR SALIDASA
            domain = [
                ('product_id', '=', product.id),
                ('state', 'in', ['done']),
                ('date', '>=', last_year_str),
                ('date', '<=', now_str),
                ('picking_type_id.code', '=', 'outgoing')
            ]

            move_lines_out = self.env['stock.move'].search(domain)

            out_qty = 0.0
            if move_lines_out:
                out_qty = sum([m.product_uom_qty for m in move_lines_out])

            # BUSCAR DEVOLUCIONES
            domain = [
                ('product_id', '=', product.id),
                ('state', 'in', ['done']),
                ('date', '>=', last_year_str),
                ('date', '<=', now_str),
                ('picking_type_id.code', '=', 'incoming'),
                ('origin_returned_move_id', '!=', False),
            ]
            move_lines_return = self.env['stock.move'].search(domain)
            return_qty = 0.0
            if move_lines_return:
                return_qty = sum(
                    [m.product_uom_qty for m in move_lines_return])

            qty = out_qty - return_qty

            product.last_year_unit_sales = qty
            product.last_year_sales = len(move_lines_out)
            product.average_month_sales = len(move_lines_out) / 12.0

            units_by_month = qty / 12.0
            if units_by_month:
                stock_months = product.qty_available / units_by_month

                product.remaining_stock_days = stock_months * 30.0


            

    
    @api.multi
    def _purchase_count(self):
        for prod in self:
            domain = [
                ('product_id', 'in', prod.ids),
            ]
            lines = self.env['purchase.order.line'].search(domain)
            prod.purchase_count = len(lines)


    purchase_count = fields.Integer(compute='_purchase_count', string='# Sales')


    last_year_sales = fields.Integer(
        'Las year sales', compute='_get_sales_info')
    average_month_sales = fields.Float(
        'Average month sales', compute='_get_sales_info')
    last_year_unit_sales = fields.Float(
        'Last year unit sales', compute='_get_sales_info')
    remaining_stock_days = fields.Float(
        'Remainig stock days', compute='_get_sales_info')
    
    @api.multi
    def action_view_purchases(self):
        self.ensure_one()
        action = self.env.ref('purchase.action_purchase_line_product_tree')

        domain = [('product_id', 'in', self.ids)]
        lines = self.env['purchase.order.line'].search(domain)

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('id', '=', lines.ids)],
        }


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.one
    def _get_pricelist_item_name_price(self):
        res = super(PricelistItem, self)._get_pricelist_item_name_price()
        # Show alwais code
        if self.product_id:
            self.name = self.product_id.display_name
        return res