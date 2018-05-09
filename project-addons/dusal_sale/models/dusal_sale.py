# -*- coding: utf-8 -*-
##############################################################################
#
#    Addons by Dusal.net
#    Copyright (C) 2016 Dusal.net Almas
#
#    Odoo Proprietary License v1.0

##############################################################################
from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    print_product_image = fields.Boolean('Print product image',
                                         readonly=False,
                                         index=True,
                                         default=True,
                                         help="If this checkbox checked then \
        print product images on Sales order & Quotation")
    image_size = fields.Selection([
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('original', 'Big')], 'Image sizes', default='small',
        help="Choose an image size here", index=True)
    print_line_number = fields.Boolean('Print line number', readonly=False,
                                       index=True, help="Print line number on \
                                       Sales order & Quotation")


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    product_image_small = fields.Binary(string='Image small',
                                        related='product_id.image_small')
    product_image_medium = fields.Binary(string='Image medium',
                                         related='product_id.image_medium')
    product_image = fields.Binary(string='Image')
