# etsygenerator/admin.py
from django.contrib import admin
from .models import Receipt, Transaction

admin.site.register(Receipt)
admin.site.register(Transaction)
