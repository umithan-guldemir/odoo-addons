# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Product Category",
    "summary": "Add description to product category",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "license": "AGPL-3",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        "views/product_public_category_view.xml",
        "templates/product_category_description.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_product_category/static/src/css/readmore.css",
        ],
    },
    "installable": True,
}
