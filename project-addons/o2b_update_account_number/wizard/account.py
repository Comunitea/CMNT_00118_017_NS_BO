# -*- encoding: utf-8 -*-
from odoo import api, models


class AccountAccountUpdate(models.TransientModel):
    _name = 'account.account.update'

    @api.multi
    def account_code_update(self):
        res = self.env['account.account'].search([])
        for account in res:
            if account.code and len(account.code) == 6 and \
                    account.type == 'other':
                code = str(account.code) + '0'
                query = "UPDATE account_account set code=" + code + \
                    "' where id='" + str(account.id) + "'"
                self.env.cr.execute(query)

        return True
