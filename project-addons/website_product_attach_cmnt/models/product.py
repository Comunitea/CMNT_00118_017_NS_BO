# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_attachments_for_website(self):
        attachment_data = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', 'in', self.ids), ('public', '=', True)])
        return attachment_data