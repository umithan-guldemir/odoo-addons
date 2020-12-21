# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    mersis = fields.Char(string="Mersis No")
    commercial_id_no = fields.Char(string="Commercial Identity No")
    tax_office_name = fields.Char(string="Tax Office")


    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + \
            ['mersis', 'commercial_id_no', 'tax_office_name']

