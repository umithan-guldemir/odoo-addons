# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "SMS OTP TurkeySMS",
    "summary": "Allow users to login with SMS OTP.",
    "version": "16.0.1.0.0",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": [
        "base",
    ],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "views/res_config_views.xml",
    ],
    "installable": True,
}
