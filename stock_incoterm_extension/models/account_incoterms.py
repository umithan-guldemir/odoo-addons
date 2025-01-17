# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountIncoterms(models.Model):
    _inherit = "account.incoterms"

    destination_port = fields.Boolean(string="Requires destination port")
    transport_type = fields.Boolean(string="Requires transport type")
