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
        'account_due_dates_str'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "views/invoice.xml",
        "views/report_invoice.xml",
        "views/sale_view.xml",
        "views/pos_report.xml",
        "views/product_view.xml",
        "wizard/change_pos_price_view.xml",
        "views/point_of_sale_view.xml",
        "views/report_sale_order.xml",
        'views/report_sessionsummary.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
