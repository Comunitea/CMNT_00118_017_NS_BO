# -*- coding: utf-8 -*-
# © 2018 Comunitea
# Ruben Seijas <ruben@comunitea.com> - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#
##############################################################################
#
#    Copyright (C) {year} {company} All Rights Reserved
#    ${developer} <{mail}>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': 'Licenses: Theme Adds Clarico',
    'version': '1.0',
    'summary': 'Tema addicional para Clarico Theme',
    'description': 'Modifica y adapta el tema Clarico Theme a las necesidades del sitio web',
    'author': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'category': 'Custom',
    'contributors': [
        "Comunitea ",
        "Ruben Seijas <ruben@comunitea.com>",
        "Pavel Smirnov <pavel@comunitea.com>"
    ],
    'depends': [
        'website_sale',
        'website_cookie_notice',
        'website_product_tags_73lines',
        'website_crm_recaptcha',
        'website_mail_channel',
        'payment_acquirer_by_amount',
        'payment_redsys',
        'payment_paypal',
        'website_sale_one_step_checkout_delivery',
        'website_sale_one_step_checkout_charge_payment_fee',
        'website_sale_require_legal',
        'website_crm_privacy_policy',
        'theme_clarico'
    ],
    'data': [
        'data/product_data.xml',
        'views/cart.xml',
        'views/product.xml',
        'views/wishlist.xml',
        'views/blog.xml',
        'views/pages.xml',
        'views/menu.xml',
        'views/shop_home.xml',
        'views/contactus.xml',
        'views/footer.xml',
        'views/header.xml',
        'views/views.xml',
        'views/product_view.xml',
        'views/account.xml',
        'views/group.xml',
        'views/terms.xml',
        'views/category_view.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
