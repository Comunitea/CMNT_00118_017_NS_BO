# -*- coding: utf-8 -*-
# Copyright 2015 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale All Report",
    "version": "10.0.1.0.0",
    "author": "Comunitea",
    'website': 'www.counitea.com',
    "category": "Sales",
    "description": """Allow to add advance payments on sales and then use its on invoices""",
    "depends": ["base", "sale", "account","sales_team"],
    "data": ['views/sale_all_report.xml',
             'views/res_partner_views.xml',
             'security/sale_security.xml',
             'security/ir.model.access.csv',
             ],
    "installable": True,
}
