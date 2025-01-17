# Copyright 2025 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Split Stock Move Picking",
    "summary": """
       Splits stock.move record in pickings.
       """,
    "author": "yibudak, Altinkaya Enclosures",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "category": "Product",
    "license": "LGPL-3",
    "version": "16.0.1.0.0",
    "depends": ["base", "stock"],
    "data": [
        "wizard/wizard_split_picking_line.xml",
        "views/stock_picking_view.xml",
        "security/ir.model.access.csv",
    ],
}
