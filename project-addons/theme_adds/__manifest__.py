# -*- coding: utf-8 -*-
# © 2018 Comunitea
# Ruben Seijas <ruben@comunitea.com> - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Theme Adds Clarico',
    'version': '1.0',
    'summary': 'Tema addicional para Clarico Theme',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'category': 'Custom',
    'depends': [
        'website_sale',
        'website_cookie_notice',
        'website_product_tags_73lines',
        'website_crm_recaptcha',
        'website_mail_channel',
        'website_sale_one_step_checkout',
        'website_sale_one_step_checkout_delivery',
        'payment_redsys',
        'payment_paypal',
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
    'images': [
        'static/description/icon.png',
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
