# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

# Copyright 2025 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ReportAccountMoveLine(models.TransientModel):
    _name = "report.account.move.line"
    _description = "Wizard for report.account.move.line"
    _inherit = "xlsx.report"

    # Report Result, account.move.line
    results = fields.Many2many(
        comodel_name="account.move.line",
        string="Move Lines",
        compute="_compute_move_lines",
        help="Use compute fields, so there is nothing stored in database",
    )

    def _compute_move_lines(self):
        selected_ids = self.env.context.get("active_ids", [])
        ids = self.env["account.move.line"].browse(selected_ids)
        for rec in self:
            rec.results = ids
