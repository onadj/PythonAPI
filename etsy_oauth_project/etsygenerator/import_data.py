import os
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from etsygenerator.models import Receipt, Transaction, Refund, Shipment

def import_data():
    # Path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), "receipts_response.json")

    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    with transaction.atomic():
        for receipt_data in data.get("receipts", []):
            import_receipt(receipt_data)
            
        try:
            receipt = Receipt.objects.get(receipt_id=receipt_data["receipt_id"])
        except ObjectDoesNotExist:
            receipt = Receipt(receipt_id=receipt_data["receipt_id"])
            receipt.receipt_type = receipt_data.get("receipt_type", 0)
            receipt.seller_user_id = receipt_data.get("seller_user_id", 0)
            receipt.seller_email = receipt_data.get("seller_email", "")
            receipt.buyer_user_id = receipt_data.get("buyer_user_id", 0)
            receipt.buyer_email = receipt_data.get("buyer_email", "")
            receipt.name = receipt_data.get("name", "")
            receipt.first_line = receipt_data.get("first_line", "")
            receipt.second_line = receipt_data.get("second_line", "")
            receipt.city = receipt_data.get("city", "")
            receipt.state = receipt_data.get("state", "")
            receipt.zip = receipt_data.get("zip", "")
            receipt.status = receipt_data.get("status", "")
            receipt.formatted_address = receipt_data.get("formatted_address", "")
            receipt.country_iso = receipt_data.get("country_iso", "")
            receipt.payment_method = receipt_data.get("payment_method", "")
            receipt.payment_email = receipt_data.get("payment_email", "")
            receipt.message_from_payment = receipt_data.get("message_from_payment", "")
            receipt.message_from_seller = receipt_data.get("message_from_seller", "")
            receipt.message_from_buyer = receipt_data.get("message_from_buyer", "")
            receipt.is_shipped = receipt_data.get("is_shipped", False)
            receipt.is_paid = receipt_data.get("is_paid", False)
            receipt.create_timestamp = receipt_data.get("create_timestamp", 0)
            receipt.created_timestamp = receipt_data.get("created_timestamp", 0)
            receipt.update_timestamp = receipt_data.get("update_timestamp", 0)
            receipt.updated_timestamp = receipt_data.get("updated_timestamp", 0)
            receipt.is_gift = receipt_data.get("is_gift", False)
            receipt.gift_message = receipt_data.get("gift_message", "")

            # Nested fields
            receipt.grandtotal_amount = receipt_data.get("grandtotal_amount", 0.0)
            receipt.grandtotal_divisor = receipt_data.get("grandtotal_divisor", 1)
            receipt.grandtotal_currency_code = receipt_data.get("grandtotal_currency_code", "USD")
            receipt.subtotal_amount = receipt_data.get("subtotal_amount", 0.0)
            receipt.subtotal_divisor = receipt_data.get("subtotal_divisor", 1)
            receipt.subtotal_currency_code = receipt_data.get("subtotal_currency_code", "USD")
            receipt.total_price_amount = receipt_data.get("total_price_amount", 0.0)
            receipt.total_price_divisor = receipt_data.get("total_price_divisor", 1)
            receipt.total_price_currency_code = receipt_data.get("total_price_currency_code", "USD")

            receipt.save()

            # Import transactions, refunds, and shipments
            import_transactions(receipt, receipt_data.get("transactions", []))
            import_refunds(receipt, receipt_data.get("refunds", []))
            import_shipments(receipt, receipt_data.get("shipments", []))

def import_transactions(receipt, transactions_data):
    for transaction_data in transactions_data:
        # Use a more meaningful field for uniqueness, e.g., a combination of fields
        unique_identifier = {"receipt": receipt, "transaction_id": transaction_data["transaction_id"]}
        Transaction.objects.update_or_create(
            defaults={
                "title": transaction_data.get("title", ""),
                "description": transaction_data.get("description", ""),
                "seller_user_id": transaction_data.get("seller_user_id", 0),
                "buyer_user_id": transaction_data.get("buyer_user_id", 0),
                "create_timestamp": transaction_data.get("create_timestamp", 0),
                "created_timestamp": transaction_data.get("created_timestamp", 0),
                "paid_timestamp": transaction_data.get("paid_timestamp", 0),
                "shipped_timestamp": transaction_data.get("shipped_timestamp", None),
                "quantity": transaction_data.get("quantity", 0),
                "listing_image_id": transaction_data.get("listing_image_id", 0),
                "is_digital": transaction_data.get("is_digital", False),
                "file_data": transaction_data.get("file_data", ""),
                "listing_id": transaction_data.get("listing_id", 0),
                "sku": transaction_data.get("sku", ""),
                "product_id": transaction_data.get("product_id", 0),
                "transaction_type": transaction_data.get("transaction_type", ""),
                "price": transaction_data.get("price", 0.0),
                "shipping_cost": transaction_data.get("shipping_cost", 0.0),
                "variations": transaction_data.get("variations", {}),
                "product_data": transaction_data.get("product_data", {}),
                "shipping_profile_id": transaction_data.get("shipping_profile_id", 0),
                "min_processing_days": transaction_data.get("min_processing_days", 0),
                "max_processing_days": transaction_data.get("max_processing_days", 0),
                "shipping_method": transaction_data.get("shipping_method", ""),
                "shipping_upgrade": transaction_data.get("shipping_upgrade", ""),
                "expected_ship_date": transaction_data.get("expected_ship_date", None),
                "buyer_coupon": transaction_data.get("buyer_coupon", 0),
                "shop_coupon": transaction_data.get("shop_coupon", 0),
            },
            **unique_identifier
        )

def import_refunds(receipt, refunds_data):
    for refund_data in refunds_data:
        # Use a more meaningful field for uniqueness, e.g., a combination of fields
        unique_identifier = {"receipt": receipt, "reason": refund_data["reason"]}
        Refund.objects.update_or_create(
            defaults={
                "note_from_issuer": refund_data.get("note_from_issuer", ""),
                "status": refund_data.get("status", ""),
                "amount": refund_data.get("amount", 0.0),
                "created_timestamp": refund_data.get("created_timestamp", 0),
            },
            **unique_identifier
        )

def import_shipments(receipt, shipments_data):
    for shipment_data in shipments_data:
        # Use a more meaningful field for uniqueness, e.g., a combination of fields
        unique_identifier = {"receipt": receipt, "receipt_shipping_id": shipment_data["receipt_shipping_id"]}
        Shipment.objects.update_or_create(
            defaults={
                "shipment_notification_timestamp": shipment_data.get("shipment_notification_timestamp", 0),
                "carrier_name": shipment_data.get("carrier_name", ""),
                "tracking_code": shipment_data.get("tracking_code", ""),
            },
            **unique_identifier
        )

if __name__ == "__main__":
    import_data()
