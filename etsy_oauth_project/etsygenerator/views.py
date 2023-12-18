# views.py
import os
import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Receipt, Transaction  # Import your models

def refresh_tokens():
    refresh_command = "python refreshtoken.py"
    os.system(refresh_command)

    with open("tokens.txt", "r") as file:
        lines = file.readlines()
        new_access_token = lines[0].split(":")[1].strip()
        new_token_type = lines[1].split(":")[1].strip()
        new_expires_in = lines[2].split(":")[1].strip()
        new_refresh_token = lines[3].split(":")[1].strip()

    return new_access_token, new_token_type, new_expires_in, new_refresh_token

def run_etsy_script(request):
    shop_id = "34038896"
    new_access_token, new_token_type, new_expires_in, new_refresh_token = refresh_tokens()

    get_receipts_command = f"python getShopReceipts.py {new_access_token} {new_token_type} {new_expires_in} {new_refresh_token} {shop_id}"
    response = os.popen(get_receipts_command).read()

    try:
        json_response = json.loads(response)
    except json.JSONDecodeError as e:
        return HttpResponse(f"Error decoding JSON: {e}\nRaw response: {response}", status=500)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = "receipts_response.json"
    file_path = os.path.join(script_dir, "etsygenerator", relative_path)

    with open(file_path, "w") as json_file:
        json.dump(json_response, json_file, indent=4)

    return HttpResponse("Etsy script executed successfully!", status=200)

def upload_json(request):
    if request.method == 'POST':
        # Assuming you have a form with a file input for JSON upload
        uploaded_file = request.FILES.get('json_file')

        if uploaded_file:
            # Process the uploaded JSON file
            try:
                json_data = json.loads(uploaded_file.read().decode('utf-8'))
                
                # Your logic to save data to the database or perform other actions

                return HttpResponse("JSON file uploaded and processed successfully!", status=200)

            except json.JSONDecodeError as e:
                return HttpResponse(f"Error decoding JSON: {e}", status=400)

    return HttpResponse("Invalid request or missing JSON file.", status=400)

def import_to_database(request):
    # File path to the JSON file (assuming it's in the etsy_oauth_project folder)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "receipts_response.json")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Iterate through the data and create Receipt, Transaction, and Refund records
        for receipt_data in data.get('receipts', []):
            receipt = Receipt.objects.create(**receipt_data)
            transactions_data = receipt_data.get('transactions', [])
            for transaction_data in transactions_data:
                transaction = Transaction.objects.create(receipt=receipt, **transaction_data)

                refunds_data = transaction_data.get('refunds', [])
                for refund_data in refunds_data:
                    Refund.objects.create(receipt=receipt, transaction=transaction, **refund_data)

        return HttpResponse("Data imported successfully.")
    except Exception as e:
        return HttpResponse(f"Error importing data: {e}", status=500)

def display_receipts(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})

def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipts/receipt_list.html', {'receipts': receipts})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})
