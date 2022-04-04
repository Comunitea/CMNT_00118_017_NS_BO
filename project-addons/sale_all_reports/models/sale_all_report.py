# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models


class SaleAllReport(models.Model):
    _name = "sale.all.report"
    _description = "All Orders Statistics"
    _auto = False

    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    date = fields.Datetime('Date Order', readonly=True)
    product_uom_qty = fields.Float('# of Qty', readonly=True)
    price_total = fields.Float('Total', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)


    def _select(self):
        select_str = """
             SELECT min(sol.id) as id,
             sol.product_id as product_id,
             pts.categ_id as categ_id,
             ss.partner_id as partner_id,
             ss.user_id as user_id,
             ss.company_id as company_id,
             ss.date_order as date,
             SUM(sol.price_total) as price_total,
             SUM(sol.product_uom_qty) as product_uom_qty,
             SUM(sol.price_subtotal) as price_subtotal
        """
        return select_str

    def _select2(self):
        select_str = """
             SELECT min(pol.id) as id,
             product_id as product_id,
             ptp.categ_id as categ_id,
             s.partner_id as partner_id,
             s.user_id as user_id,
             s.company_id as company_id,
             s.date_order as date,
             SUM((pol.qty * pol.price_unit) * (100 - pol.discount) / 100) AS price_total,
             SUM(pol.qty) as product_uom_qty,
             SUM(pol.price_subtotal) as price_subtotal
        """
        return select_str

    def _from(self):
        from_str = """
            sale_order_line sol
                LEFT JOIN pos_order ss ON (ss.id=sol.order_id)
                LEFT JOIN product_product ps ON (sol.product_id=ps.id)
                LEFT JOIN product_template pts ON (ps.product_tmpl_id=pts.id)
                LEFT JOIN product_uom us ON (us.id=pts.uom_id)
                LEFT JOIN res_partner spartner on ss.partner_id = spartner.id
        """
        return from_str
    def _from2(self):
        from_str = """
            pos_order_line pol
                LEFT JOIN pos_order s ON (s.id=pol.order_id)
                LEFT JOIN product_product p ON (pol.product_id=p.id)
                LEFT JOIN product_template ptp ON (p.product_tmpl_id=ptp.id)
                LEFT JOIN product_uom u ON (u.id=ptp.uom_id)
                LEFT JOIN res_partner ppartner on s.partner_id = ppartner.id
        """
        return from_str


    def _group_by(self):
        group_by_str = """
            GROUP BY sol.product_id,
                     pts.categ_id,
                     ss.partner_id,
                     ss.user_id,
                     ss.company_id,
                     ss.date_order
        """
        return group_by_str
    def _group_by2(self):
        group_by_str = """
            GROUP BY pol.product_id,
                     ptp.categ_id,
                     s.partner_id,
                     s.user_id,
                     s.company_id,
                     s.date_order
        """
        return group_by_str
    @api.model_cr
    def init(self):
        # self._table = sale_all_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            UNION
            %s
            FROM %s
            %s
            )""" % (self._table, self._select(), self._from(),self._group_by(), self._select2(), self._from2(), self._group_by2())
        print(query)
        self.env.cr.execute(query)
