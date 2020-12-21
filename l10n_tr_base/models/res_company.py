# -*- coding: utf-8 -*-
'''
@author: Codequarters - Grey
'''

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    mersis = fields.Char(related='partner_id.mersis', readonly=False)
    commercial_id_no = fields.Char(related='partner_id.commercial_id_no', readonly=False)
    tax_office_name = fields.Char(related='partner_id.tax_office_name', readonly=False)

