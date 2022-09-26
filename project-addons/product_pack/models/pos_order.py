from odoo import models,fields

class PosOrder(models.Model):

    _inherit = "pos.order"

    def create_picking(self):
        res = super(PosOrder,self).create_picking()
        for pos in self.filtered('picking_id') :
            for move in pos.picking_id.move_lines:
                if move.product_id.pack:
                    for pl in move.product_id.pack_line_ids:
                        subproduct = pl.product_id
                        self.env['stock.move'].create({
                            'name': '> ' + subproduct.name,
                            'product_uom': subproduct.uom_id.id,
                            'picking_id': pos.picking_id.id ,
                            'picking_type_id': pos.picking_id.picking_type_id.id ,
                            'product_id': subproduct.id,
                            'product_uom_qty': abs(pl.quantity * move.product_uom_qty),
                            'state': 'draft',
                            'location_id': move.location_id.id ,
                            'location_dest_id': move.location_dest_id.id,
                        })

                    pos._force_picking_done(pos.picking_id)
        return res
