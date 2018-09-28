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
        'website_sale',
        'clarico_layout'
    ],
    'data': [
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
    ],
    'images': [
        'static/description/icon.png',
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
