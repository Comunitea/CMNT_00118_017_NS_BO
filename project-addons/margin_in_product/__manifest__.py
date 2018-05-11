# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) Monoyer Fabian (info@olabs.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
    'name': "Margin in Product",
    'category': 'tools',
    'version': '1.0',
    'description': """

     Margin
     =======

     This gives the profitability by calculating the difference between the
     Price for customers and Cost Price.

        """,
    'price': 19,
    'live_test_url': 'http://custo.olabs.be/web/login?db=demo0002&login=demo',
    'currency': "EUR",
    'author': "O'Labs",
    'depends': [
        'product'
    ],
    'data': [
        'views/product.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
}
