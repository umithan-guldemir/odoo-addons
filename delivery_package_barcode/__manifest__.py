# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Delivery Package Barcode",
    "summary": "Provides fields to be able to use integration modules.",
    "author": "Yiğit Budak, Odoo Turkey Localization Group, Altinkaya Enclosures",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "license": "AGPL-3",
    "category": "Delivery",
    "version": "16.0.1.1.0",
    "depends": ["barcodes", "stock", "delivery_integration_base"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/delivery_package_barcode_wiz_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "delivery_package_barcode/static/src/js/delivery_package_barcode.js",
        ],
    },
    "installable": True,
}
