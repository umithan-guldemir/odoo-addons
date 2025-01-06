# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Catch 404 Errors",
    "summary": "Catch All 404 Errors and Log Them",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "license": "AGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/website_views.xml",
        "views/website_404_errors_views.xml",
        "views/website_rewrite_views.xml",
        "wizards/wizard_create_redirect_from_404_views.xml",
    ],
    "installable": True,
}
