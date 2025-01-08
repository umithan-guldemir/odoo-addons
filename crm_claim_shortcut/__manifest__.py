# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Copyright 2024 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "CRM Claim Shortcut",
    "summary": "CRM Claim Shortcut on Sale, Invoice, Picking",
    "version": "16.0.1.0.0",
    "development_status": "Mature",
    "category": "crm",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Yiğit Budak, Altinkaya Enclosures",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "delivery_integration_base",
        "delivery",
        "utm",
        "crm_claim",
        "sale",
        "stock",
        "account",
    ],
    "data": [
        "view/crm_claim_view.xml",
        "view/sale_order_view.xml",
        "view/account_move_view.xml",
        "view/product_product_view.xml",
        "view/stock_picking_view.xml",
    ],
}
