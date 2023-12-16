# etsygenerator/urls.py
from django.urls import path
from .views import run_etsy_script, display_receipts

urlpatterns = [
    path('run-script/', run_etsy_script, name='run_etsy_script'),
    path('display-receipts/', display_receipts, name='display_receipts'),
]
