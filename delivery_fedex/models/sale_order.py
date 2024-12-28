from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customs_value_currency_id = fields.Many2one(
        "res.currency",
        string="Customs Value Currency",
        domain="[('name', 'in', ['USD', 'EUR'])]",
    )
    customs_value = fields.Monetary(
        string="Customs Value", currency_field="customs_value_currency_id"
    )
