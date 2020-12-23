# -*- coding: utf-8 -*-
# © 2020 Comunitea - Vicente Ángel Gutiérrez <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Nostrum Custom Res Partner',
    'version': '10.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Stock",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'base_vat',
        'account',
        'account_banking_mandate',
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
    "installable": True
}
