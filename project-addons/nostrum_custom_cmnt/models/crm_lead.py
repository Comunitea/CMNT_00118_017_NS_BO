# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models
import time


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def retrieve_sales_dashboard(self):
        res = super(CrmLead, self).retrieve_sales_dashboard()
        # date_today = fields.Date.from_string(fields.Date.context_today(self))

        res['phonecall'] = {
            'today': 0,
            'next_7_days': 0,
        }
        date_next_week = datetime.today() + relativedelta(days=7)
        date_next_week_str = fields.Date.to_string(date_next_week)

        today_start = time.strftime('%Y-%m-%d') + " 00:00:00"
        today_end = time.strftime('%Y-%m-%d') + " 23:59:59"
        week_end = date_next_week_str + " 23:59:59"

        domain = [('user_id', '=', self._uid),
                  ('date', '>=', today_start),
                  ('date', '<=', today_end)]
        today_num = self.env['crm.phonecall'].search_count(domain)

        domain = [('user_id', '=', self._uid),
                  ('date', '>=', today_start),
                  ('date', '<=', week_end)]
        week_num = self.env['crm.phonecall'].search_count(domain)
        if today_num:
            res['phonecall']['today'] = today_num
        if week_num:
            res['phonecall']['next_7_days'] = week_num
        return res
