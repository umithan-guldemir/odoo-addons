{
    "name": "Turkey Addresses",
    "version": "16.0.1.0.0",
    "summary": "Add custom field in Customer like District, Region, Neighbourhood",
    "category": "Partner",
    "license": "LGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Yigit Budak, Kirankumar, Ahmet Altinisik, Altinkaya Enclosures",
    "external_dependencies": {"python": ["openpyxl", "unicode_tr"]},
    "depends": ["sale", "base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/address_details_view.xml",
        "wizard/wizard_address_import_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
