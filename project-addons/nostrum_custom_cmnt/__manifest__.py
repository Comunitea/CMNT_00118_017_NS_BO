# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Nostrum Custom Cmnt',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Stock",
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'account',
        'account_payment_partner',
        'o2b_cust_vendor_ref_com_b',
        'o2b_stock_filter',
        'indaws_nostrum_sport',
        'point_of_sale',
        'deltatech_sale_margin',
        'dusal_sale',  # Para heredar el report metiendo las imágenes,
        'account_due_dates_str',
        'stock_valued_picking_report',
        'crm_phonecall',
        'stock',
        'purchase',
        'delivery',
        'web_m2x_options',
        'stock_account',
        'sale_commission',
        'nostrum_custom_commission',
        'website_sale',
        'product_pack',
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "security/nostrum_security.xml",
        "security/ir.model.access.csv",
        'data/pos_sequence.xml',
        "views/invoice.xml",
        "views/report_invoice.xml",
        "views/sale_view.xml",
        "views/stock_view.xml",
        "views/phonecall_view.xml",
        "views/pos_report.xml",
        "views/product_view.xml",
        "wizard/change_pos_price_view.xml",
        "views/point_of_sale_view.xml",
        "views/report_sale_order.xml",
        'views/report_sessionsummary.xml',
        'views/account_view.xml',
        'views/partner_view.xml',
        'views/sale_commission_view.xml',
        "wizard/recompute_price_min_view.xml",
    ],
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/sales_team_dashboard.xml',
    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
