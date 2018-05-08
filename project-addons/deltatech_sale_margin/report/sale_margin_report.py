# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import tools
from odoo import models, api, fields


class SaleMarginReport(models.Model):
    _name = "sale.margin.report"
    _description = "Sale margin report"
    _auto = False
    _order = 'date desc'

    date = fields.Date('Date', readonly=True)
    invoice_id = fields.Many2one('account.invoice', 'Invoice', readonly=True)
    categ_id = fields.Many2one('product.category', 'Category', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom = fields.Many2one('product.uom', 'Unit of Measure',
                                  readonly=True)
    product_uom_qty = fields.Float('Quantity', readonly=True)
    sale_val = fields.Float('Sale value', readonly=True,
                            help="Sale value in company currency")
    stock_val = fields.Float("Stock value", readonly=True,
                             help="Stock value in company currency")
    profit_val = fields.Float("Profit", readonly=True,
                              help="Profit obtained at invoicing in \
                              company currency")
    commission_computed = fields.Float("Commission Computed", readonly=True)
    commission = fields.Float("Commission")
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner',
                                            'Commercial Partner',
                                            readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson')
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    period_id = fields.Many2one('account.period', 'Period', readonly=True)

    type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Supplier Invoice'),
        ('out_refund', 'Customer Refund'),
        ('in_refund', 'Supplier Refund'),
    ], 'Type', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('proforma', 'Pro-forma'),
        ('proforma2', 'Pro-forma'),
        ('open', 'Open'),
        ('paid', 'Done'),
        ('cancel', 'Cancelled')
    ], 'Invoice Status', readonly=True)

    def _select(self):
        select_str = """
                select
                    min(l.id) as id,
                    s.date_invoice as date,
                    l.invoice_id as invoice_id,
                    t.categ_id as categ_id,
                    l.product_id as product_id,
                    t.uom_id as product_uom,

                    SUM(CASE
                     WHEN s.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN -(l.quantity / u.factor * u2.factor)
                        ELSE  (l.quantity / u.factor * u2.factor)
                    END) AS product_uom_qty,

                    SUM(CASE
                     WHEN s.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN -(l.quantity * l.price_unit * (100.0-COALESCE( l.discount, 0 )) / 100.0)
                        ELSE  (l.quantity * l.price_unit * (100.0-COALESCE( l.discount, 0 )) / 100.0)
                    END) AS sale_val,

                    SUM(CASE
                     WHEN s.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN -(l.quantity * COALESCE( l.purchase_price, 0 ) )
                        ELSE  (l.quantity * COALESCE( l.purchase_price, 0 ) )
                    END) AS stock_val,

                    SUM(CASE
                     WHEN s.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN -( (l.quantity * l.price_unit * (100.0-l.discount) / 100.0) - (l.quantity * COALESCE( l.purchase_price, 0 ) ))
                        ELSE  ( (l.quantity * l.price_unit * (100.0-l.discount) / 100.0) - (l.quantity * COALESCE( l.purchase_price, 0 ) ))
                    END) AS profit_val,

                    SUM( CASE
                            WHEN s.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN -( (l.quantity * l.price_unit * (100.0-l.discount) / 100.0) - (l.quantity * COALESCE( l.purchase_price, 0 ) ))*cu.rate
                            ELSE  ( (l.quantity * l.price_unit * (100.0-l.discount) / 100.0) - (l.quantity * COALESCE( l.purchase_price, 0 ) ))*cu.rate
                        END
                    ) AS commission_computed,
                    sum(l.commission) as commission,

                    s.partner_id as partner_id,
                    s.commercial_partner_id as commercial_partner_id,
                    s.user_id as user_id,
                    s.period_id,
                    s.company_id as company_id,
                    s.type, s.state
        """
        return select_str

    def _from(self):
        from_str = """
            account_invoice s
            left join account_invoice_line l on (s.id=l.invoice_id)
            left join product_product p on (l.product_id=p.id)
            left join product_template t on (p.product_tmpl_id=t.id)
            left join product_uom u on (u.id=l.uom_id)
            left join product_uom u2 on (u2.id=t.uom_id)
            left join commission_users cu on (s.user_id = cu.user_id)
        """
        return from_str

    def _where(self):
        where_str = """
              s.type in ( 'out_invoice', 'out_refund') and s.state in
              ( 'open','paid')
        """
        return where_str

    def _group_by(self):
        group_by_str = """
                    l.product_id,
                    l.invoice_id,
                    t.uom_id,
                    t.categ_id,
                    s.date_invoice,
                    s.partner_id,
                    s.commercial_partner_id,
                    s.user_id,
                    s.company_id,
                    s.period_id,
                    s.type,
                    s.state
        """
        return group_by_str

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            WHERE %s
            GROUP BY %s
            )""" % (self._table, self._select(), self._from(), self._where(),
                    self._group_by()))

    @api.multi
    def write(self, vals):
        invoice_line = self.env['account.invoice.line'].browse(self.id)
        invoice_line.write({'commission': vals.get('commission', False)})
        if 'user_id' in vals:
            invoice = self.env['account.invoice'].browse(self.invoice_id)
            invoice.write({'user_id': vals['user_id']})
        return True
