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

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # This is the reverse link of the field 'invoice_ids' of sale.order
    # defined in addons/sale/sale.py
    sale_ids = fields.Many2many(
        'sale.order', 'sale_order_invoice_rel', 'invoice_id',
        'order_id', 'Sale Orders', readonly=True,
        help="This is the list of sale orders related to this invoice.")

    purchase_ids = fields.Many2many(
        'purchase.order', 'purchase_invoice_rel', 'invoice_id',
        'purchase_id', 'Purchase Orders', readonly=True,
        help="This is the list of purchase orders related to this invoice.")
