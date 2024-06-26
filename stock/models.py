import math
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()


class Stock(models.Model):
    company = models.CharField(max_length=200)
    price_per_bond = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    live_percent = models.CharField(max_length=30, null=True, blank=True)
    picture = CloudinaryField('image', null=True, default=None, blank=True)

    def __str__(self):
        return f"{self.company} |  ${self.price_per_bond} per bond."
    

class BuyStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_profit = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    percent_live = models.FloatField(default=0.4)
    sold_for = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.stock.company}-{self.amount}"
    
    def get_number_of_bonds(self):
        my_bond = self.amount / self.stock.price_per_bond
        return math.ceil(my_bond)
    
    def get_live_profit(self):
        if self.is_profit:
            live_profit = self.amount * Decimal(self.percent_live)
        else:
            live_profit = self.amount / Decimal(self.percent_live)
        return math.ceil(live_profit)
