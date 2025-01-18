# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

# Copyright 2025 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        """
        Set rate_type context if partner uses a
        custom rate field on Account Move creation
        """
        for vals in vals_list:
            if vals.get("partner_id"):
                partner = self.env["res.partner"].browse(vals["partner_id"])
                if partner and partner.property_rate_field != "rate":
                    self = self.with_context(rate_type=partner.property_rate_field)
        return super().create(vals_list)

    def action_post(self):
        """
        Override action_post to ensure proper currency rate is used on move creation
        """
        for move in self:
            if (
                move.partner_id.property_rate_field != "rate"
                and not move.use_custom_rate
            ):
                return super(
                    AccountMove,
                    self.with_context(rate_type=move.partner_id.property_rate_field),
                ).action_post()

        return super().action_post()
