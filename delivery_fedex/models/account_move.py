from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    carrier_id = fields.Many2one(
        "delivery.carrier",
        string="Carrier",
        copy=False,
        related="picking_ids.carrier_id",
        readonly=True,
    )
    delivery_type = fields.Selection(
        related="carrier_id.delivery_type", string="Delivery Type", readonly=True
    )

    # customs_value_currency_id = fields.Many2one(
    #     "res.currency",
    #     string="Customs Value Currency",
    #     domain="[('name', 'in', ['USD', 'EUR'])]",
    # )
    # customs_value = fields.Monetary(
    #     string="Customs Value", currency_field="customs_value_currency_id"
    # )

    def send_fedex_shipping(self):
        self.ensure_one()
        if self.carrier_id.delivery_type == "fedex":
            self.carrier_id.fedex_account_send_shipment(self)
        return True

    def get_fedex_rates(self):
        self.ensure_one()
        if self.carrier_id.delivery_type == "fedex":
            self.carrier_id.fedex_account_rate_shipment(self)
        return True
