# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Accounting chart for Turkey",
    "version": "16.0.0.1.0",
    "summary": "Chart of accounts for Turkey",
    "category": "Localization/Turkey",
    "website": "https://github.com/altinkaya-opensource/odoo-addons",
    "author": "Ahmet Altınışık, Altinkaya Enclosures",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        # TODO: Fix or delete this module
        # "data/chart_data.xml",
        # "data/account.group.csv",
        # "data/account_tag.xml",
        "data/account.account.template.csv",
        # "data/chart_template_data.xml",
        "data/chart_template.xml",
        # "data/fiscal_position_template_data.xml",
    ],
    "installable": True,
    "auto_install": False,
}
