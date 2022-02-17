# -*- coding: utf-8 -*-
# © 2022 Comunitea - Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Custom layout Nostrum',
    'version': '10.0.1.0.0',
    'summary': 'Custom modifications for the Nostrum layouts',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'category': 'Custom',
    'contributors': [
        "Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>",
    ],
    'depends': [
        'report',
    ],
    'data': [
        'data/paperformat.xml',
        'views/res_company.xml',
        'views/layout_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
