# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


{
    'name': 'Ampliaciones informes facturas',
    'version': '1.0',
    'author': 'inDAWS',
    'category': 'Tools',
    'depends': ['base', 'account', 'product', 'sale', 'purchase',
                'indaws_detalle_impuestos', 'account_invoice_line_view',
                'deltatech_sale_margin', 'point_of_sale'],
    'demo': [],
    'data': [
        'views/account_view.xml',
        'views/pos_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'views/sale_view.xml',
        'security/ir.model.access.csv'],
    'installable': True,
}
