# -*- coding: utf-8 -*-
# © 2021 Comunitea - Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields

class AcquirerRedsys(models.Model):
    _inherit = 'payment.acquirer'

    redsys_pay_method = fields.Selection(selection_add=[('z', 'Pago con Móvil')])