from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    exact_fedex_price = fields.Float(
        default=0.0,
    )

    tracking_ref = fields.Char(string="Tracking Reference", copy=False)

    def fedex_get_label(self):
        return None  # TODO
