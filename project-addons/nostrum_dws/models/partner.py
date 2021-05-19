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

        dws_reminder_mail = self.env['ir.config_parameter'].get_param("nostrum_dws.dws_reminder_mail")

        if not dws_reminder_mail:
            logger.error(_('Days without shopping failed: The dws_reminder_mail parameter is undefined. Check them in ir.config.parameter.'))
            return        

        partner_ids = self.env['res.partner'].search([
            ("last_website_so_id", "!=", False),
            ("last_website_so_id.confirmation_date", "!=", False)
        ])

        mail_line = ''
        for partner in partner_ids:
            dws = (datetime.now() - datetime.strptime(partner.last_website_so_id.confirmation_date, DEFAULT_SERVER_DATETIME_FORMAT)).days
            if dws and dws > partner.dws_reminder_days:
                mail_line += "<li>{} - Días desde su última compra ({}): {}</li>".format(partner.display_name, partner.last_website_so_id.confirmation_date, dws)
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
                logger.error(_('Days without shopping succedd: Created the mail: {}.'.format(res)))
            except ImportError as e:
                logger.error(_('Days without shopping failed: {}.'.format(e)))
