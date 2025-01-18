# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

# Copyright 2025 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("currency_id", "date_order")
    def _compute_sale_currency_rate(self):
        for order in self:
            currency_id = order.currency_id or order.env.user.company_id.currency_id
            if order.partner_id and order.partner_id.property_rate_field != "rate":
                curr_dict = currency_id.with_context(
                    rate_type=order.partner_id.property_rate_field
                )._get_rates(order.env.user.company_id, order.date_order)
            else:
                curr_dict = currency_id._get_rates(
                    order.env.user.company_id, order.date_order
                )
            order.sale_currency_rate = 1 / curr_dict.get(currency_id.id, 1.0)
        return True
