# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
import logging
logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    valued_picking = fields.Boolean(default=False)
    pay_invoice_days = fields.Integer(
        'Average payment invoice days', readonly=True)
    pay_due_days = fields.Integer(
        'Average payment dues days', readonly=True)

    @api.model
    def _get_partners_to_process(self):
        """
        Devuelve los partners con efectos nuevos desde la fecha de última
        ejecución
        """
        ConfigParameter = self.env['ir.config_parameter']
        last_check = ConfigParameter.get_param(
            'diff.days.last.check', '1990-01-01')

        query = """
        select distinct(partner_id) 
        from account_move_line aml
        inner join account_account aa on aa.id = aml.account_id
        where aml.pay_date > '%s'
        and aml.invoice_id is not null
        and aml.partner_id is not null
        and aa.internal_type = 'receivable'
        and aml.reconciled = True
        """ % last_check
        self._cr.execute(query)
        partner_ids = self._cr.fetchall()
        return self.browse([x[0] for x in partner_ids])

    @api.model
    def process_pay_diff_days(self):
        """
        Función del cron que calcula para cada partner la media de
        los campos de los días previamente calculados en los computes de 
        account.move.lines
        """
        partners = self._get_partners_to_process()
        len_partners = len(partners)
        i = 0
        for partner in partners:
            i += 1
            logger.info("PROCESS partner diff days: %s/%s" % (i, len_partners))

            # el reconciled = true creo que no lo necesito
            query = """
                select avg(diff_invoice_days), 
                avg(diff_due_days)
                from account_move_line aml
                inner join account_account aa on aa.id = aml.account_id
                and aml.invoice_id is not null
                and aml.partner_id = %s
                and aml.diff_invoice_days is not null
                and aml.diff_due_days is not null
                and aa.internal_type = 'receivable'
            """ % partner.id
            self._cr.execute(query)
            res = self._cr.fetchall()
            if not res:
                continue
            avg1, avg2 = res[0]
            partner.write({
                'pay_invoice_days': avg1,
                'pay_due_days': avg2,
            })

        self.env['ir.config_parameter'].set_param(
            'diff.days.last.check', fields.Datetime.now())
        return True
