# -*- coding: utf-8 -*-
# © 2019 Comunitea Servicios Tecnológicos S.L. <javier@comunitea.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

import time


class CrmPhonecall2phonecall(models.TransientModel):
    _inherit = 'crm.phonecall2phonecall'
    _description = 'Phonecall To Phonecall'

  

    @api.model
    def default_get(self, fields):
        """
        This function gets default values

        """
        res = super(CrmPhonecall2phonecall, self).default_get(fields)
        res.update({
            'name': 'Seguimiento?',
        })
        return res
