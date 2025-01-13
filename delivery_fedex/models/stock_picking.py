from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    exact_fedex_price = fields.Float(
        string="Exact Fedex Price",
        default=0.0,
    )

    tracking_ref = fields.Char(string="Tracking Reference", copy=False)

    def fedex_get_label(self):
        return None  # TODO
