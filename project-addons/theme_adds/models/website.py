# -*- coding: utf-8 -*-
# © 2018 Comunitea - Pavel Seijas <ruben@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    social_instagram = fields.Char('Instagram Account')


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    website_id = fields.Many2one('website', string="website", default=1, required=True)
    social_instagram = fields.Char(related='website_id.social_instagram')
    domain = fields.Char(related='website_id.domain')
