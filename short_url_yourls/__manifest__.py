# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Copyright 2024 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Short URL Yourls",
    "summary": "YOURLS (FOSS URL shortener service) integration, see yourls.org",
    "version": "16.0.1.0.0",
    "development_status": "Mature",
    "category": "Tools",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "queue_job", "iap"],
    "data": [
        "view/short_url_yourls_view.xml",
        "security/ir.model.access.csv",
    ],
}
