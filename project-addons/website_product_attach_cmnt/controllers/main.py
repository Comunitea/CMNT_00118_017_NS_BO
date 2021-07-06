# -*- coding: utf-8 -*-
# © 2018 Comunitea - Comunitea - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import base64
from cStringIO import StringIO
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from odoo.addons.website_portal.controllers.main import website_account


class ProductAttachments(website_account):

    @http.route([
        '/my/productAtt/<int:attachment_id>',
    ], type='http', auth='public')
    def download_attachment(self, attachment_id=None):
        # Check if this is a valid attachment id
        
        if not attachment_id:
            return redirect('/shop')

        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "file_type", "res_model", "res_id", "type", "url"]
        )

        if attachment:
            attachment = attachment[0]
        else:
            return redirect('/shop')

        # Check attachment model
        res_model = attachment['res_model']

        if res_model not in ['product.product', 'product.template']:
            return redirect('/shop')

        if attachment["datas"]:
            data = StringIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'].encode('utf-8'), as_attachment=True)
        else:
            return request.not_found()
