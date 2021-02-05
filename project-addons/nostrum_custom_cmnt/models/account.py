# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api
import logging
logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.journal'

    # To create a invoice with the selected payment mode
    payment_mode_id = fields.Many2one(
        'account.payment.mode', string='Payment Mode',
        domain=[('payment_type', '=', 'inbound')])


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pay_due_days = fields.Integer(
        'Average payment dues days', related="partner_id.pay_due_days",
        store=True)
    pay_date = fields.Date('Payment date', compute='_get_payment_date', 
                           store=True)
    diff_invoice_days = fields.Integer(
        'Days from invoice date', readonly=True, 
        compute='_get_payment_date', store=True)
    diff_due_days = fields.Integer(
        'Days from due date', readonly=True, 
        compute='_get_payment_date', store=True)

    @api.depends('full_reconcile_id', 'matched_credit_ids')
    def _get_payment_date(self):
        """
        Cada vez que se hace una conciliacion total o parcial, encontrar el 
        efecto que lo paga y anotar su fecha como fecha de pago, de paso 
        calcular los días para que el cron haga la media
        """
        len_self = len(self)
        i = 0
        for ml in self:
            i += 1
            logger.info(
                "PROCESS pay date in move: %s/%s" % (i, len_self))
            #  EL CAMPO RECONCILED_LINE_IDS es muy lento
            # if not ml.reconcile_line_ids or ml.pay_date or not ml.invoice_id:
            reconciled_lines = ml._get_reconciled_lines()
            if not reconciled_lines or not ml.invoice_id \
                    or not ml.date or not ml.date_maturity:
                continue
            r_mls = reconciled_lines.filtered(
                lambda m: m.id != ml.id and not m.invoice_id)
            pay_move = False

            # Si es reconciliacion paracial:
            # Como solo me interesan efectos de factura de la 4300
            # deben tener el campo débito > 0, por lo que accedo al objeto
            # reconciliacion parcial y cojo el credit_move_id
            if len(r_mls) > 1: 
                if ml.matched_credit_ids:
                    # Cojo el mas nuevo de los parciales,
                    # para el caso de un efecto que queda a medio pagar
                    # coger la fecha del último pago
                    pay_move = ml.matched_credit_ids.\
                        sorted('id', reverse=True)[0].credit_move_id
                else:
                    pau_move = r_mls[0]
            else:
                pay_move = r_mls
            if pay_move:
                payment_date = fields.Date.from_string(pay_move.date)
                move_date = fields.Date.from_string(ml.date)
                move_date_due = fields.Date.from_string(ml.date_maturity)
                diff1 = (payment_date - move_date).days
                diff2 = (payment_date - move_date_due).days
                ml.update({
                    'pay_date': pay_move.date,
                    'diff_invoice_days': diff1,
                    'diff_due_days': diff2,
                })
