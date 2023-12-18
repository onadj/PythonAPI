# etsygenerator/urls.py
from django.urls import path
from .views import run_etsy_script

urlpatterns = [
    path('run-script/', run_etsy_script, name='run_etsy_script'),
    
]
