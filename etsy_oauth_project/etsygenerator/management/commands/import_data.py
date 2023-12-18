# import_data.py
import json
from django.core.management.base import BaseCommand
from etsygenerator.models import Receipt, Transaction, Price, Shipment
from datetime import datetime

class Command(BaseCommand):
    help = 'Import data from JSON file'

    def handle(self, *args, **options):
        with open('receipts_response.json', 'r') as file:
            data = json.load(file)

        for result in data.get('results', []):
            self.import_receipt(result)

    def import_receipt(self, data):
        # Extract data for Receipt model
        receipt_data = {
            'receipt_id': data.get('receipt_id'),
            'receipt_type': data.get('receipt_type'),
            'seller_user_id': data.get('seller_user_id'),
            'seller_email': data.get('seller_email'),
            'buyer_user_id': data.get('buyer_user_id'),
            'buyer_email': data.get('buyer_email'),
            'name': data.get('name'),
            'first_line': data.get('first_line'),
            'second_line': data.get('second_line'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip': data.get('zip'),
            'status': data.get('status'),
            'formatted_address': data.get('formatted_address'),
            'country_iso': data.get('country_iso'),
            'payment_method': data.get('payment_method'),
            'payment_email': data.get('payment_email'),
            'message_from_payment': data.get('message_from_payment'),
            'message_from_seller': data.get('message_from_seller'),
            'message_from_buyer': data.get('message_from_buyer'),
            'is_shipped': data.get('is_shipped'),
            'is_paid': data.get('is_paid'),
            'create_timestamp': self.parse_timestamp(data.get('create_timestamp')),
            'created_timestamp': self.parse_timestamp(data.get('created_timestamp')),
            'update_timestamp': self.parse_timestamp(data.get('update_timestamp')),
            'updated_timestamp': self.parse_timestamp(data.get('updated_timestamp')),
            'is_gift': data.get('is_gift'),
            'gift_message': data.get('gift_message'),
        }

        # Extract and create/update Price object for grandtotal
        grandtotal_data = data.get('grandtotal')
        grandtotal, _ = Price.objects.get_or_create(**grandtotal_data)
        receipt_data['grandtotal'] = grandtotal

        # Extract and create/update Price object for subtotal
        subtotal_data = data.get('subtotal')
        subtotal, _ = Price.objects.get_or_create(**subtotal_data)
        receipt_data['subtotal'] = subtotal

        # Extract and create/update Price object for total_price
        total_price_data = data.get('total_price')
        total_price, _ = Price.objects.get_or_create(**total_price_data)
        receipt_data['total_price'] = total_price

        # Create or update the Receipt instance
          try:
            receipt = Receipt.objects.get(receipt_id=receipt_data['receipt_id'])
            # Update existing receipt with new data
            for key, value in receipt_data.items():
                setattr(receipt, key, value)
            receipt.save()
              except Receipt.DoesNotExist:
            # Create a new receipt if it doesn't exist
            receipt = Receipt.objects.create(**receipt_data)

        # Import associated transactions
        transactions_data = data.get('transactions', [])
        for transaction_data in transactions_data:
            self.import_transaction(receipt, transaction_data)

    def import_transaction(self, receipt, data):
        # Extract data for Transaction model
        transaction_data = {
            'transaction_id': data.get('transaction_id'),
            'title': data.get('title'),
            'description': data.get('description'),
            'seller_user_id': data.get('seller_user_id'),
            'buyer_user_id': data.get('buyer_user_id'),
            'create_timestamp': self.parse_timestamp(data.get('create_timestamp')),
            'created_timestamp': self.parse_timestamp(data.get('created_timestamp')),
            'paid_timestamp': self.parse_timestamp(data.get('paid_timestamp')),
            'shipped_timestamp': self.parse_timestamp(data.get('shipped_timestamp')),
            'quantity': data.get('quantity'),
            'listing_image_id': data.get('listing_image_id'),
            'receipt': receipt,
            'is_digital': data.get('is_digital'),
            'file_data': data.get('file_data'),
            'listing_id': data.get('listing_id'),
            'sku': data.get('sku'),
            'product_id': data.get('product_id'),
            'transaction_type': data.get('transaction_type'),
            'variations': data.get('variations'),
            'product_data': data.get('product_data'),
            'shipping_profile_id': data.get('shipping_profile_id'),
            'min_processing_days': data.get('min_processing_days'),
            'max_processing_days': data.get('max_processing_days'),
            'shipping_method': data.get('shipping_method'),
            'shipping_upgrade': data.get('shipping_upgrade'),
            'expected_ship_date': self.parse_timestamp(data.get('expected_ship_date')),
            'buyer_coupon': data.get('buyer_coupon'),
            'shop_coupon': data.get('shop_coupon'),
        }

        # Extract and create/update Price object for price
        price_data = data.get('price', {})
        price_instance, _ = Price.objects.get_or_create(**price_data)
        transaction_data['price'] = price_instance

        # Extract and create/update Price object for shipping_cost
        shipping_cost_data = data.get('shipping_cost', {})
        shipping_cost_instance, _ = Price.objects.get_or_create(**shipping_cost_data)
        transaction_data['shipping_cost'] = shipping_cost_instance

        # Create or update the Transaction instance
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_data['transaction_id'])
            for key, value in transaction_data.items():
                setattr(transaction, key, value)
            transaction.save()
        except Transaction.DoesNotExist:
            transaction = Transaction.objects.create(**transaction_data)

    def parse_timestamp(self, timestamp_str):
        # Check if timestamp is already a datetime object (int or datetime)
        if isinstance(timestamp_str, (int, datetime)):
            return timestamp_str
        # Parse timestamp string to datetime object
        if timestamp_str:
            return datetime.fromtimestamp(int(timestamp_str))
        return None
