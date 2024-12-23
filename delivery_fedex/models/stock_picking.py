from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    customs_value_currency_id = fields.Many2one('res.currency', string="Customs Value Currency", default=lambda self: self.env.ref('base.USD'))
    customs_value = fields.Monetary(string="Customs Value", currency_field='customs_value_currency_id')

    delivery_rate_currency_id = fields.Many2one('res.currency', string="Delivery Rate Currency", default=lambda self: self.env.ref('base.USD'), readonly=True)
    delivery_rate = fields.Monetary(string="Delivery Rate", currency_field='delivery_rate_currency_id', readonly=True)



    def fedex_get_label(self):
        return None

    def fedex_get_rate(self):
        self.ensure_one()
        rate_data = self.carrier_id._fedex_get_rate(self)
        self.delivery_rate_currency_id = self.env.ref('base.{currency}'.format(currency=rate_data["currency"]))
        self.delivery_rate = rate_data["price"]
