from odoo import tools
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    all_order_count = fields.Integer(compute='_compute_all_order_count', string='# of Sales Order')

    def _compute_all_order_count(self):
        all_partners = self.search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        sale_order_groups = self.env['sale.order'].read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            fields=['partner_id'], groupby=['partner_id']
        )
        pos_order_groups = self.env['pos.order'].read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            fields=['partner_id'], groupby=['partner_id']
        )
        for group in sale_order_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.all_order_count += group['partner_id_count']
                partner = partner.parent_id

        for group in pos_order_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.all_order_count += group['partner_id_count']
                partner = partner.parent_id

