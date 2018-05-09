# -*- encoding: utf-8 -*-
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def update_account_receivable(self):
        if self.customer_ref and self.property_account_receivable_id:
            account_recc = self.property_account_receivable_id
            customer_ref = self.customer_ref
            new_customer_ref = customer_ref[:4]
            code = account_recc.code
            new_code = code[:3]
            updated_code = new_code + new_customer_ref
            new_account_recc = account_recc.copy()
            print "new_account_recc", new_account_recc
            new_account_recc.write({'code': updated_code, 'name': self.name})
            self.write({'property_account_receivable_id': new_account_recc.id})
        return True

    @api.multi
    def update_account_payable(self):
        if self.vendor_ref and self.property_account_payable_id:
            account_pay = self.property_account_payable_id
            vendor_ref = self.vendor_ref
            new_vendor_ref = vendor_ref[:4]
            code = account_pay.code
            new_code = code[:3]
            updated_code = new_code + new_vendor_ref
            new_account_pay = account_pay.copy()
            print "new_account_pay", new_account_pay
            new_account_pay.write({'code': updated_code, 'name': self.name})
            self.write({'property_account_payable_id': new_account_pay.id})
        return True
