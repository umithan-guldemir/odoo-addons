from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    log_id = fields.Many2one(
        comodel_name="ir.logging",
        string="Related Log",
    )
