from django.contrib import admin

from .models import Stock, BuyStock, BuySoldStock

admin.site.register(Stock)
admin.site.register(BuyStock)
admin.site.register(BuySoldStock)
