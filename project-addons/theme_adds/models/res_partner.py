# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class Partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id), ('website_available', '=', True)]}}
        else:
            return {'domain': {'state_id': [('website_available', '=', True)]}}
