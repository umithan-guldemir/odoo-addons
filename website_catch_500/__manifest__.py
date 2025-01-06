# Copyright 2024 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Catch 500 Errors",
    "summary": "Catch All 500 Errors and Log Them",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Ismail Cagan Yilmaz, Altinkaya Enclosures",
    "license": "LGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "category": "Extensions",
    "depends": ["base", "website", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/website_views.xml",
        "views/website_500_errors_views.xml",
    ],
    "installable": True,
}
