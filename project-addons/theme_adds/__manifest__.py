# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Theme Adds Clarico',
    'version': '1.0',
    'summary': 'Tema addicional para Clarico Theme',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'category': 'Custom',
    'depends': [
        'clarico_shop',
        'website_sale',
        'clarico_layout',
        'website_product_tags_73lines'
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
    ],
    'images': [
        'static/description/icon.png',
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
