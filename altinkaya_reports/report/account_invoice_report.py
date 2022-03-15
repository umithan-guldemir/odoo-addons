from odoo import models, fields, api, tools


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    usd_rate = fields.Float('USD Rate', compute='_compute_usd_rate', store=True, default=1.0)

    @api.multi
    @api.depends('date_invoice', 'currency_id')
    def _compute_usd_rate(self):
        currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        for ai in self:
            date_invoice = ai.date_invoice
            try:
                ai.currency_rate = ai.currency_id.with_context(date=date_invoice).rate or 1.0
                ai.usd_rate = currency_usd.with_context(date=date_invoice).rate or 1.0
            except Exception:
                pass

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    state_id = fields.Many2one('res.country.state', string='State', readonly=True)
    price_total_usd = fields.Float(string='Untaxed Total USD', readonly=True)
    price_average_usd = fields.Float(string='Average Price USD', readonly=True, group_operator="avg")

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
               ", sub.state_id, sub.price_total_usd as price_total_usd, sub.price_average_usd as price_average_usd"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + \
               """, coalesce(partner.state_id, partner_ai.state_id) AS state_id,
               SUM(ail.price_subtotal_signed * invoice_type.sign * ai.usd_rate) AS price_total_usd,
               sum(abs(ail.price_subtotal_signed) * ai.usd_rate) /
                CASE
                    WHEN sum(ail.quantity / COALESCE(u.factor, 1::numeric) * COALESCE(u2.factor, 1::numeric)) <> 0::numeric THEN sum(ail.quantity / COALESCE(u.factor, 1::numeric) * COALESCE(u2.factor, 1::numeric))
                    ELSE 1::numeric
                END AS price_average_usd"""

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", coalesce(partner.state_id, partner_ai.state_id)"

