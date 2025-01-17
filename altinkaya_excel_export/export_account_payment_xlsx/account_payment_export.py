# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

# Copyright 2025 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ReportAccountPayment(models.TransientModel):
    _name = "report.account.payment"
    _description = "Wizard for report.account.payment"
    _inherit = "xlsx.report"

    # Report Result, account.invoice
    results = fields.Many2many(
        comodel_name="account.payment",
        string="Payments",
        compute="_compute_payments",
        help="Use compute fields, so there is nothing stored in database",
    )

    def _compute_payments(self):
        selected_ids = self.env.context.get("active_ids", [])
        ids = self.env["account.payment"].browse(selected_ids)
        for rec in self:
            rec.results = ids
