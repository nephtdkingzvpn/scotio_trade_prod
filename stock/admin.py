from django.contrib import admin

from .models import Stock, BuyStock

admin.site.register(Stock)
admin.site.register(BuyStock)
