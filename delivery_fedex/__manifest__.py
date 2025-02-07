{
    "name": "Delivery FedEx",
    "summary": "Delivery Carrier implementation for FedEx API",
    "version": "16.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Altinkaya Enclosures",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "sale",
        "delivery",
        "delivery_state",
        "delivery_package_number",
        "delivery_price_method",
    ],
    "external_dependencies": {"python": ["requests", "json"]},
    "data": [
        "views/delivery_fedex_view.xml",
        "views/stock_picking_views.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "wizard/choose_delivery_carrier.xml",
    ],
}
