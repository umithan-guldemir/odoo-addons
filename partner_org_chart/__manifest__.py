# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Partner Organization Chart",
    "summary": "Organization chart on partner form",
    "license": "LGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Ümithan Güldemir, Altinkaya Enclosures",
    "category": "CRM",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    "data": [
        "views/partner_views.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "partner_org_chart/static/src/scss/variables.scss",
        ],
        "web.assets_backend": [
            "partner_org_chart/static/src/fields/*",
        ],
    },
}
