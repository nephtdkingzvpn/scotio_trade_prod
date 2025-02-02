from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# my imports
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    dollar_balance = models.DecimalField(decimal_places=2, max_digits=12, default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    picture = CloudinaryField('image', null=True, default=None, blank=True)
    charge_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.full_name
    

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bitcoin = models.FloatField(default=0.0)
    etheriun = models.FloatField(default=0.0)
    usdt = models.DecimalField(decimal_places=2, max_digits=12, default=0)

    def __str__(self):
        return self.user.profile.full_name

    
    
@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)


class BankAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank = models.CharField(max_length=200)
    holder_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    swift_iban = models.CharField(max_length=100, null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.holder_name} - {self.bank}"
    

class BankTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank = models.CharField(max_length=200)
    holder_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    swift_iban = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.holder_name} - {self.bank}"

    

