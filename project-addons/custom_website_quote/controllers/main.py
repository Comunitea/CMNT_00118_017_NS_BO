# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http, _
from odoo.http import request
from odoo.addons.website_quote.controllers.main import sale_quote


class SaleQuoteCustom(sale_quote):
    @http.route(
        "/quote/<int:order_id>/<token>",
        type="http",
        auth="public",
        website=True,
    )
    def view(self, order_id, pdf=None, token=None, message=False, **post):
        new_ctxt = dict(request.env.context)
        new_ctxt.update({"quote_payments": True, "order_price": order_id})
        request.env.context = new_ctxt
        res = super(SaleQuoteCustom, self).view(
            order_id, pdf, token, message, **post
        )
        return res

    @http.route(
        ["/quote/<int:order_id>/transaction/<int:acquirer_id>/<token>"],
        type="json",
        auth="public",
        website=True,
    )
    def payment_transaction_token(self, acquirer_id, order_id, token):
        request.session["sale_last_order_id"] = order_id

        PaymentTransaction = request.env["payment.transaction"].sudo()

        Order = request.env["sale.order"].sudo().browse(order_id)
        if not Order or not Order.order_line or acquirer_id is None:
            return request.redirect("/quote/%s" % order_id)

        # find an already existing transaction
        Transaction = PaymentTransaction.create(
            {
                "acquirer_id": acquirer_id,
                "type": Order._get_payment_type(),
                "amount": Order.amount_total,
                "currency_id": Order.pricelist_id.currency_id.id,
                "partner_id": Order.partner_id.id,
                "reference": PaymentTransaction.get_next_reference(Order.name),
                "sale_order_id": Order.id,
                "callback_eval": "self.sale_order_id._confirm_online_quote(self)",
            }
        )
        request.session["quote_%s_transaction_id" % Order.id] = Transaction.id

        # update quotation
        Order.write(
            {
                "payment_acquirer_id": acquirer_id,
                "payment_tx_id": Transaction.id,
            }
        )

        return Transaction.acquirer_id.with_context(
            submit_class="btn btn-primary", submit_txt=("Pay & Confirm")
        ).render(
            Transaction.reference,
            Order.amount_total,
            Order.pricelist_id.currency_id.id,
            values={
                "return_url": "/quote/%s/%s" % (order_id, token)
                if token
                else "/quote/%s" % order_id,
                "type": Order._get_payment_type(),
                "alias_usage": _(
                    "If we store your payment information on our server, subscription payments will be made automatically."
                ),
                "partner_id": Order.partner_shipping_id.id
                or Order.partner_invoice_id.id,
                "billing_partner_id": Order.partner_invoice_id.id,
            },
        )
        return super(SaleQuoteCustom, self).payment_transaction_token(
            acquirer_id, order_id, token
        )
