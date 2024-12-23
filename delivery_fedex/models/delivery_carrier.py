from odoo import fields, models
from .fedex_request import FedExRequest

FEDEX_SERVICES = [
    ("INTERNATIONAL_ECONOMY", "International Economy"),
    ("INTERNATIONAL_FIRST", "International First"),
    ("INTERNATIONAL_PRIORITY", "International Priority"),
    ("INTERNATIONAL_PRIORITY_EXPRESS", "International Priority Express"),
]

FEDEX_PICKUP_TYPES = [("DROPOFF_AT_FEDEX_LOCATION", "Dropoff at FedEx location")]

FEDEX_PAYMENT_TYPES = [
    ("SENDER", "Sender"),
    ("RECIPIENT", "Recipient"),
    ("THIRD_PARTY", "Third Party"),
    ("COLLECT", "Collect"),
]

FEDEX_CARRIER_CODE = [
    ("FDXE", "FedEx Express"),
    ("FDXG", "FedEx Ground"),
    ("FXSP", "FedEx SmartPost"),
    ("FXCC", "FedEx Custom Critical"),
]

FEDEX_SHIPMENT_PURPOSES = [
    ("SOLD", "Sold"),
    ("NOT_SOLD", "Not Sold"),
    ("PERSONAL_EFFECTS", "Personal Effects"),
    ("GIFT", "Gift"),
    ("SAMPLE", "Sample"),
    ("REPAIR_AND_RETURN", "Repair and Return"),
    ("RETURN_AND_REPAIR", "Return and Repair"),
    ("COMMERCIAL", "Commercial"),
    ("PERSONAL_USE", "Personal Use"),
]


FEDEX_UOM_CODES = {
    "Units": "Ea",
}


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"
    delivery_type = fields.Selection(
        selection_add=[("fedex", "FedEx")],
        ondelete={"fedex": "set default"},
    )
    fedex_client_id = fields.Char(string="Client ID", help="FedEx Client ID")
    fedex_client_secret = fields.Char(
        string="Client Secret", help="FedEx Client Secret"
    )
    fedex_account_number = fields.Integer(
        string="Account Number", help="FedEx Account Number"
    )

    service_type = fields.Selection(selection=FEDEX_SERVICES, string="Service Type")
    pickup_type = fields.Selection(selection=FEDEX_PICKUP_TYPES, string="Pickup Type")
    payment_type = fields.Selection(
        selection=FEDEX_PAYMENT_TYPES, string="Payment Type"
    )
    document_shipment = fields.Boolean(string="Document Shipment")
    shipment_purpose = fields.Selection(
        selection=FEDEX_SHIPMENT_PURPOSES, string="Shipment Purpose"
    )
    customs_payment_type = fields.Selection(
        selection=FEDEX_PAYMENT_TYPES, string="Customs Payment Type"
    )
    customer_fedex_number = fields.Integer(
        selection=FEDEX_PAYMENT_TYPES, string="Customer FedEx Number"
    )

    carrier_code = fields.Selection(selection=FEDEX_CARRIER_CODE, string="Carrier Code")

    def _prepare_address(self, partner):
        return {
            "streetLines": [partner.street],
            "city": partner.city,
            "postalCode": partner.zip,
            "countryCode": partner.country_id.code,
            "residential": False,
        }

    # WORK ON
    def _prepare_contact(self, partner):
        return {
            "personName": partner.name,
            "phoneNumber": partner.phone or "+34123456789",
            "emailAddress": partner.email,
            "companyName": partner.name,
        }

    def _prepare_packages_data(self, pickings):
        packages = []

        dummy_dimensions = {"length": 10, "width": 10, "height": 10, "units": "CM"}

        for pack in pickings:
            packages.append(
                {
                    "weight": {"units": "KG", "value": pack._get_estimated_weight()},
                    "dimensions": dummy_dimensions,
                }
            )

        return packages

    def _prepare_sales_customs_data(self, order_lines):
        data = {
            "dutiesPayment": {
                "paymentType": self.customs_payment_type,
                "payor": {
                    "responsibleParty": {
                        "accountNumber": {
                            "value": str(self.fedex_account_number)
                            if self.customs_payment_type == "SENDER"
                            else str(self.customer_fedex_number)
                        },
                        "contact": self._prepare_contact(order_lines.company_id)
                        if self.customs_payment_type == "SENDER"
                        else self._prepare_contact(order_lines.partner_id),
                        "address": self._prepare_address(order_lines.company_id)
                        if self.customs_payment_type == "SENDER"
                        else self._prepare_address(order_lines.partner_id),
                    }
                },
            },
            "commodities": [],
            "commercialInvoice": {
                "purpose": self.shipment_purpose,
            },
        }

        order_lines.ensure_one()
        for order_line in order_lines._get_lines_impacting_invoice_status():
            if order_line._is_not_sellable_line():
                continue

            data["commodities"].append(
                {
                    "customsValue": {
                        "currency": order_lines.customs_value_currency_id.name,
                        "amount": str(order_lines.customs_value),
                    },
                    "description": order_line.product_id.name,
                    "name": order_line.product_id.name,
                    "countryOfManufacture": order_line.product_id.country_of_origin.code,
                    "quantity": order_line.qty_to_deliver,
                    "harmonizedCode": order_line.product_id.hs_code,
                    "quantityUnits": FEDEX_UOM_CODES[order_line.product_id.uom_name],
                    # "weight": {
                    #     "units": "KG",
                    #     "value": pickings.custom_total_weight # WORK ON
                    # }
                }
            )

        return data

    def _prepare_account_customs_data(self, pickings):
        data = {
            "dutiesPayment": {
                "paymentType": self.customs_payment_type,
                "payor": {
                    "responsibleParty": {
                        "accountNumber": {
                            "value": str(self.fedex_account_number)
                            if self.customs_payment_type == "SENDER"
                            else str(self.customer_fedex_number)
                        },
                        "contact": self._prepare_contact(pickings.company_id)
                        if self.customs_payment_type == "SENDER"
                        else self._prepare_contact(pickings.partner_id),
                        "address": self._prepare_address(pickings.company_id)
                        if self.customs_payment_type == "SENDER"
                        else self._prepare_address(pickings.partner_id),
                    }
                },
            },
            "commodities": [],
            "totalCustomsValue": {"currency": "EUR", "amount": 150},
            "commercialInvoice": {
                "purpose": self.shipment_purpose,
            },
        }
        # picking.move_ids
        for picking in pickings:
            if picking.invoice_state == "2binvoiced":
                continue
            for package in pickings.package_ids:
                data["commodities"].append(
                    {
                        "customsValue": {
                            "currency": "EUR",  # pickings.customs_value_currency_id.name,
                            "amount": "150",  # str(pickings.customs_value),
                        },
                        "unitPrice": {"amount": "100", "currency": "EUR"},
                        "description": picking.move_ids.product_id.name,
                        "name": picking.move_ids.product_id.name,
                        "countryOfManufacture": picking.move_ids.product_id.country_of_origin.code,
                        "quantity": picking.move_ids.quantity_done,
                        "harmonizedCode": picking.move_ids.product_id.hs_code,
                        "quantityUnits": FEDEX_UOM_CODES[
                            picking.move_ids.product_id.uom_name
                        ],
                        "weight": {"units": "KG", "value": package.shipping_weight},
                    }
                )

        return data

    def _prepare_sales_rate_data(self, pickings):
        data = {
            "accountNumber": {"value": str(self.fedex_account_number)},
            "requestedShipment": {
                "shipper": {"address": self._prepare_address(pickings.company_id)},
                "recipient": {"address": self._prepare_address(pickings.partner_id)},
                "serviceType": self.service_type,
                "preferredCurrency": pickings.company_id.currency_id.display_name,
                "rateRequestType": ["PREFERRED"],
                "pickupType": self.pickup_type,
                "packagingType": "YOUR_PACKAGING",
                "shipDateStamp": pickings.expected_date.strftime("%Y-%m-%d"),
                "documentShipment": self.document_shipment,
                "requestedPackageLineItems": [],
            },
            "carrierCodes": [self.carrier_code],
        }

        data["requestedShipment"]["requestedPackageLineItems"] = (
            self._prepare_packages_data(pickings)
        )
        data["requestedShipment"]["customsClearanceDetail"] = (
            self._prepare_sales_customs_data(pickings)
        )

        return data

    def _prepare_account_rate_data(self, account_move):
        data = {
            "accountNumber": {"value": str(self.fedex_account_number)},
            "requestedShipment": {
                "shipper": {"address": self._prepare_address(account_move.company_id)},
                "recipient": {
                    "address": self._prepare_address(account_move.partner_id)
                },
                "serviceType": self.service_type,
                "preferredCurrency": account_move.company_id.currency_id.display_name,
                "rateRequestType": ["PREFERRED"],
                "pickupType": self.pickup_type,
                "packagingType": "YOUR_PACKAGING",
                "shipDateStamp": account_move.date.strftime("%Y-%m-%d"),
                "documentShipment": self.document_shipment,
                "requestedPackageLineItems": [],
            },
            "carrierCodes": [self.carrier_code],
        }

        packages = []
        total_weight = 0
        for picking in account_move.picking_ids:
            if picking.invoice_state == "2binvoiced":  # ASK
                continue

            for pack in picking.package_ids:
                packages.append(
                    {
                        "weight": {"units": "KG", "value": pack.shipping_weight},
                        "dimensions": {
                            "length": pack.package_type_id.packaging_length / 10,
                            "width": pack.package_type_id.width / 10,
                            "height": pack.package_type_id.height / 10,
                            "units": "CM",
                        },
                        # "declaredValue": {
                        #     "currency": account_move.customs_value_currency_id.name,
                        #     "amount": account_move.customs_value
                        # }
                    }
                )

            total_weight += pack.shipping_weight

        data["requestedShipment"]["totalWeight"] = total_weight

        data["requestedShipment"]["requestedPackageLineItems"] = packages

        data["requestedShipment"]["customsClearanceDetail"] = (
            self._prepare_account_customs_data(account_move.picking_ids)
        )

        return data

    def _prepare_shipment_data(self, account_move):
        base_data = {
            "accountNumber": {"value": str(self.fedex_account_number)},
            "shipAction": "CONFIRM",
            "requestedShipment": {
                "shipper": {
                    "address": self._prepare_address(account_move.company_id),
                    "contact": self._prepare_contact(account_move.company_id),
                },
                "origin": {
                    "address": self._prepare_address(account_move.company_id),
                    "contact": self._prepare_contact(account_move.company_id),
                },
                "soldTo": {
                    "address": self._prepare_address(account_move.partner_id),
                    "contact": self._prepare_contact(account_move.partner_id),
                },
                "recipients": [
                    {
                        "address": self._prepare_address(account_move.partner_id),
                        "contact": self._prepare_contact(account_move.partner_id),
                    }
                ],
                "serviceType": self.service_type,
                "preferredCurrency": account_move.company_id.currency_id.display_name,
                "shipTimestamp": account_move.date.strftime("%Y-%m-%d"),
                "rateRequestType": ["PREFERRED"],
                "pickupType": self.pickup_type,
                "packagingType": "YOUR_PACKAGING",
                "shippingChargesPayment": {
                    "paymentType": self.payment_type,
                    "payor": {
                        "responsibleParty": {
                            "address": self._prepare_address(account_move.company_id)
                            if self.payment_type == "SENDER"
                            else self._prepare_address(account_move.partner_id),
                            "accountNumber": {
                                "value": str(self.fedex_account_number)
                                if self.payment_type == "SENDER"
                                else str(self.customer_fedex_number)
                            },
                            "contact": self._prepare_contact(account_move.company_id)
                            if self.payment_type == "SENDER"
                            else self._prepare_contact(account_move.partner_id),
                        }
                    },
                },
                "customsClearanceDetail": {},
                "labelSpecification": {
                    "labelFormatType": "COMMON2D",
                    "imageType": "PDF",
                    "labelStockType": "PAPER_LETTER",
                },
                "requestedPackageLineItems": [],
            },
            "labelResponseOptions": "URL_ONLY",
            "mergeLabelDocOption": "LABELS_AND_DOCS",
        }

        packages = []
        total_weight = 0
        for picking in account_move.picking_ids:
            if picking.invoice_state == "2binvoiced":
                continue

            for pack in picking.package_ids:
                packages.append(
                    {
                        "weight": {"units": "KG", "value": pack.shipping_weight},
                        "dimensions": {
                            "length": pack.package_type_id.packaging_length / 10,
                            "width": pack.package_type_id.width / 10,
                            "height": pack.package_type_id.height / 10,
                            "units": "CM",
                        },
                        # "declaredValue": {
                        #     "currency": "EUR",  # account_move.customs_value_currency_id.name,
                        #     "amount": 150.0,  # account_move.customs_value
                        #     # / len(picking.package_ids),
                        # },
                    }
                )

            total_weight += pack.shipping_weight

        base_data["requestedShipment"]["totalWeight"] = total_weight
        base_data["requestedShipment"]["customsClearanceDetail"] = (
            self._prepare_account_customs_data(account_move.picking_ids)
        )
        base_data["requestedShipment"]["requestedPackageLineItems"] = packages

        base_data["requestedShipment"]["totalPackageCount"] = len(packages)

        return base_data

    def _fedex_send_shipment(self, account_move):
        fedex_request = FedExRequest(
            client_id=self.fedex_client_id, client_secret=self.fedex_client_secret
        )
        payload = self._prepare_shipment_data(account_move)
        result = fedex_request.create_shipment(payload)

        return result

    def fedex_account_rate_shipment(self, account_move):  # Called in account.move
        fedex_request = FedExRequest(
            client_id=self.fedex_client_id, client_secret=self.fedex_client_secret
        )
        payload = self._prepare_account_rate_data(account_move)
        rate_data = fedex_request.get_rates(payload)

        self.env["account.move.line"].create(
            {
                "move_id": account_move.id,
                "name": "FedEx Shipping",
                "quantity": 1,
                "price_unit": rate_data.get("price"),
                "product_id": account_move.carrier_id.product_id.id,
            }
        )

    def fedex_account_send_shipment(self, account_move):  # Called in account.move
        fedex_request = FedExRequest(
            client_id=self.fedex_client_id, client_secret=self.fedex_client_secret
        )
        payload = self._prepare_shipment_data(account_move)
        rate_data = fedex_request.create_shipment(payload)

        print(rate_data)

        self.env["account.move.line"].create(
            {
                "move_id": account_move.id,
                "name": "FedEx Shipping",
                "quantity": 1,
                "price_unit": rate_data.get("price"),
                "product_id": account_move.carrier_id.product_id.id,
            }
        )

    def fedex_rate_shipment(self, pickings):  # Called in sale.order
        fedex_request = FedExRequest(
            client_id=self.fedex_client_id, client_secret=self.fedex_client_secret
        )
        payload = self._prepare_sales_rate_data(pickings)
        rate_data = fedex_request.get_rates(payload)

        result = {
            "success": True,
            "price": rate_data.get("price"),
            "error_message": False,
            "warning_message": False,
        }

        return result

    def fedex_send_shipping(self, account_move):  # Called in stock.picking -> unused
        fedex_request = FedExRequest(
            client_id=self.fedex_client_id, client_secret=self.fedex_client_secret
        )
        payload = self._prepare_shipment_data(account_move)
        rate_data = fedex_request.create_shipment(payload)

        price = rate_data["output"]["pieceResponses"]["netRateAmount"]
        tracking_number = int(rate_data["output"]["masterTrackingNumber"])

        labels = []
        for package in rate_data["output"]["pieceResponses"]["packageDocuments"]:
            labels.append(
                {
                    "package_id": package["trackingNumber"],
                    "name": "Label",
                    "datas": package["label"],
                    "file_type": "PDF",
                    "tracking_number": tracking_number,
                }
            )

        return {
            "exact_price": rate_data.get(""),
            "tracking_number": "number",
            "labels": [
                {
                    "package_id": package_id,
                    "name": filename,
                    "datas": file_content(base64),
                    "file_type": extension,
                    "tracking_number": package_number,
                }
            ],
        }
