# -*- coding: utf-8 -*-
{
    'name': 'OSC Custom',
    'version': '10.0.1.0.0',
    'summary': 'Customization for OSC',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'category': 'Custom',
    'contributors': [
        "Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>",
    ],
    'depends': [
        'website_sale_one_step_checkout',
        'website_sale_one_step_checkout_delivery',
        'website_sale_one_step_checkout_charge_payment_fee',
        'theme_adds',
    ],
    'data': [
        'views/checkout.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
