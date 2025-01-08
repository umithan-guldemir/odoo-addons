# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import models
from odoo import api, SUPERUSER_ID, _
import logging

_logger = logging.getLogger(__name__)


def compute_total_quant_cost(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    empty_cost_quants = env["stock.quant"].search([])
    currency = env["res.currency"].search([("name", "=", "USD")], limit=1).id
    prec = env["decimal.precision"].precision_get("Product Unit of Measure")
    _logger.info(f"Computing total cost for {len(empty_cost_quants)} quants")
    for quant in empty_cost_quants:
        unit_cost = round(quant.product_id._get_price_from_bom(), prec)
        total_cost = round(quant.quantity * unit_cost, prec)
        cr.execute(
            """
            UPDATE stock_quant sq
            SET total_cost = %s, unit_cost = %s,
                             cost_currency_id = %s
            WHERE sq.id = %s
        """,
            (total_cost, unit_cost, currency, quant.id),
        )
        (
            _logger.info(
                _(
                    "Cost for quant %(quant_id)s is computed: %(total_cost)s",
                    quant_id=quant.id,
                    total_cost=total_cost,
                ),
            )
        )
