# -*- encoding: utf-8 -*-
from odoo import api, models


class DescriptionUpdate(models.Model):
    _name = 'description.update'

    @api.multi
    def button_update(self):
        print"Starting...."
        sale_obj = self.env["sale.order"].search([])
        inv_obj = self.env["account.invoice"].search([])
        po_obj = self.env["purchase.order"].search([])
        for line in sale_obj:
            for line1 in line.order_line:
                if line1.product_id:
                    line1.write({'name': line1.product_id.name})

        for line in inv_obj:
            for line1 in line.invoice_line:
                if line1.product_id:
                    line1.write({'name': line1.product_id.name})
        for line in po_obj:
            for line1 in line.order_line:
                if line1.product_id:
                    line1.write({'name': line1.product_id.name})
