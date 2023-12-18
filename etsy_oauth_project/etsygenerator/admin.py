# admin.py
from django.contrib import admin
from .models import RawJSON

class RawJSONAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')
    readonly_fields = ('id', 'data')
    search_fields = ('id',)

admin.site.register(RawJSON, RawJSONAdmin)
