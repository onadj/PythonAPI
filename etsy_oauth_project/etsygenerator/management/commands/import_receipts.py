# import_receipts.py

import os
import sys
import json
from django.core.management.base import BaseCommand

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HPEgenerator.settings")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Adjust the path based on your project structure

# Now you can import Django modules
from etsygenerator.models import Receipt, Transaction

class Command(BaseCommand):
    help = 'Import receipts from JSON file'

    def handle(self, *args, **options):
        # Adjust the path based on your project structure
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'receipts_response.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

            # Process the JSON data and save to the database
            for entry in data:
                receipt_data = entry['receipt']  # Adjust based on your JSON structure
                transactions_data = entry['transactions']

                # Create or update Receipt instance
                receipt, created = Receipt.objects.update_or_create(
                    receipt_id=receipt_data['receipt_id'],
                    defaults=receipt_data
                )

                # Create or update Transaction instances
                for transaction_data in transactions_data:
                    transaction, created = Transaction.objects.update_or_create(
                        transaction_id=transaction_data['transaction_id'],
                        defaults={
                            'receipt': receipt,
                            **transaction_data  # Adjust based on your JSON structure
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
