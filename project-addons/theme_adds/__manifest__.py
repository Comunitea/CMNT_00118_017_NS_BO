# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Tema addicional para Clarico Theme',
    'version': '1.0',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'category': 'Custom',
    'depends': ['website_sale',
                # 'clarico_product_carousel',
                'clarico_layout',
                'clarico_shop',
                'snippet_style_7'
                ],
    'data': [
        'views/menu.xml',
        'views/shop_home.xml',
        'views/contactus.xml',
        'views/footer.xml',
        'views/header.xml',
        'views/views.xml',
        'data/data.xml'
    ],
    'demo': [

    ],
    'installable': True,
}
