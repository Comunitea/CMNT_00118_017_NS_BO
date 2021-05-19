# -*- coding: utf-8 -*-
# © 2021 Comunitea - Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Nostrum DWS',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'website_sale',
    ],
    'contributors': [
        "Comunitea ",
        "Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>"
    ],
    "data": [
        'data/ir_config_parameter.xml',
        'data/dws_reminder_cron.xml',
        'views/partner_view.xml',
    ],
    'qweb': [],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
