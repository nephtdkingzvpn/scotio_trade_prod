from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BitcoinTrade(models.Model):
    pass


class ExchangeTrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_type = models.CharField(max_length=100)
    crypto_amt = models.FloatField()
    dollar_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.exchange_type