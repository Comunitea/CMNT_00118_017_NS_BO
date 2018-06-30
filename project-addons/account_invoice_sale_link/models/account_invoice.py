# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Sale Link module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _get_sales(self):
        """
        Get sales related to invoice lines
        """
        for invoice in self:
            sale_ids = invoice.invoice_line_ids.\
                mapped('sale_line_ids.order_id')
            invoice.update({
                'sale_ids': sale_ids
            })

    sale_ids = fields.Many2many(
        'sale.order', 'Sale Orders', compute="_get_sales", readonly=True,
        help="This is the list of sale orders related to this invoice.")


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # The reverse relation
    sale_line_ids = fields.Many2many(
        'sale.order.line', 'sale_order_line_invoice_rel', 'invoice_line_id',
        'order_line_id', 'Sale Orders', readonly=True,
        help="This is the list of sale orders related to this invoice.")
