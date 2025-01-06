# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ALTINKAYA MRP Extension",
    "summary": "Extra features for MRP Module",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "license": "AGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "category": "Extensions",
    "depends": ["mrp", "product", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_template_line_views.xml",
    ],
    "installable": True,
}
