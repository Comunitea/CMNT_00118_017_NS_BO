# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields

class BlogPost(models.Model):
    _inherit = 'blog.post'

    blog_post_image = fields.Char('Background Image URL', default='')
