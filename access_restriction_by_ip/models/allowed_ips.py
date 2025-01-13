##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import ipaddress

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    allowed_ips = fields.One2many("allowed.ips", "users_ip", string="IP")


class AllowedIPs(models.Model):
    _name = "allowed.ips"
    _description = "Allowed IP address for Odoo Login"

    users_ip = fields.Many2one("res.users", string="IP")
    ip_address = fields.Char(string="Allowed IP")

    @api.constrains("ip_address")
    def _check_ip(self):
        for rec in self:
            if rec.ip_address:
                try:
                    ipaddress.ip_network(rec.ip_address)
                except ValueError:
                    raise ValidationError(  # noqa: B904
                        _(
                            "Please enter a valid IP address or"
                            " subnet mask (%(ip_addr)s)",
                            ip_addr=rec.ip_address,
                        )
                    )
