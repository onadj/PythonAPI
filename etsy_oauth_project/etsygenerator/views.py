# etsygenerator/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Receipt, Transaction
from .your_script_file import run_your_script_function  # Import the function to run your Etsy script

def run_etsy_script(request):
    # Call your Etsy script function here
    run_your_script_function()

    # Optionally, you can return a response to indicate success or redirect to another page
    return HttpResponse("Etsy script executed successfully!")

def display_receipts(request):
    # Retrieve and display receipts (adjust as needed)
    receipts = Receipt.objects.all()
    return render(request, 'etsygenerator/receipts.html', {'receipts': receipts})
