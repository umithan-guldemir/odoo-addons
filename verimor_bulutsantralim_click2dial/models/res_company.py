# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Copyright 2024 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    bulutsantralim_connector_id = fields.Many2one(
        "bulutsantralim.connector",
        string="Bulutsantralim Connector",
        copy=False,
        help="Bulutsantralim connector for this company.",
    )
