# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Stock Incoterm Extension",
    "version": "16.0.0.1.0",
    "license": "AGPL-3",
    "depends": ["stock_account", "sale_stock", "purchase"],
    "author": "OdooMRP team," "AvanzOSC," "Serv. Tecnol. Avanzados - Pedro M. Baeza" "Ümithan Güldemir",
    "website": "http://www.odoomrp.com",
    "category": "Stock",
    "data": [
        "security/ir.model.access.csv",
        "views/account_incoterm_view.xml",
        "views/stock_view.xml",
        "views/account_move_view.xml",
        "views/sale_order_view.xml",
        # "views/purchase_order_view.xml"
    ],
    "installable": True,
    "auto_install": False,
}
