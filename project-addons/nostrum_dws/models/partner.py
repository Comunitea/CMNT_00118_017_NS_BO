# -*- coding: utf-8 -*-
# © 2021 Comunitea - Vicente Ángel Gutiérrez Fernández <vicente@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _
from datetime import date, datetime, time, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import logging
logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    dws_reminder_days = fields.Integer(
        'Days without shopping reminder', default=90)

    def dws_reminder(self):

        def _get_last_confirmation_date(sale_order_ids):
            last_confirmation_date = False
            for sale_order in sale_order_ids:
                if sale_order.confirmation_date and (not last_confirmation_date or sale_order.confirmation_date > last_confirmation_date):
                    last_confirmation_date = sale_order.confirmation_date
            return last_confirmation_date

        dws_reminder_mail = self.env['ir.config_parameter'].get_param("nostrum_dws.dws_reminder_mail")
        all_sales = self.env['ir.config_parameter'].get_param("nostrum_dws.all_sales")

        if not dws_reminder_mail:
            logger.error(_('Days without shopping failed: The dws_reminder_mail parameter is undefined. Check them in ir.config.parameter.'))
            return

        # All sale orders
        if all_sales:
            partner_ids = self.env['res.partner'].search([
                ("sale_order_ids", "!=", False),
            ])
        else:
            # Only website orders
            partner_ids = self.env['res.partner'].search([
                ("last_website_so_id", "!=", False),
                ("last_website_so_id.confirmation_date", "!=", False)
            ])

        mail_line = ''
        for partner in partner_ids:
            last_confirmation_date = _get_last_confirmation_date(partner.sale_order_ids)
            if all_sales and last_confirmation_date:
                dws = (datetime.now() - datetime.strptime(last_confirmation_date, DEFAULT_SERVER_DATETIME_FORMAT)).days
                if dws and dws == partner.dws_reminder_days:
                    mail_line += "<li>{} - Días desde su última compra ({}): {}</li>".format(partner.display_name.encode('utf-8'), last_confirmation_date, dws)
            if not all_sales:
                dws = (datetime.now() - datetime.strptime(partner.last_website_so_id.confirmation_date, DEFAULT_SERVER_DATETIME_FORMAT)).days
                if dws and dws == partner.dws_reminder_days:
                    mail_line += "<li>{} - Días desde su última compra ({}): {}</li>".format(partner.display_name.encode('utf-8'), partner.last_website_so_id.confirmation_date, dws)
        if mail_line:
            body = 'Los siguientes usuarios han superado el tiempo de aviso sin realizar compras: <ul>%s</ul>'%mail_line
            subject = 'Aviso de usuarios que han superado el tiempo sin comprar'

            try:
                mail_obj = self.env['mail.mail'].sudo()

                res = mail_obj.create({
                    'email_to': dws_reminder_mail,
                    'email_from': 'info@nostrumsport.com',
                    'lang': self.env.user.lang,
                    'subject': subject,
                    'body_html': '<pre>%s</pre>' % body
                })
                logger.info(_('Days without shopping succedd: Created the mail: {}.'.format(res)))
            except ImportError as e:
                logger.error(_('Days without shopping failed: {}.'.format(e)))
