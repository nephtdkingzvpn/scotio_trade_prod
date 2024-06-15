from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

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
    dollar_balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bitcoin = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    etheriun = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    usdt = models.DecimalField(decimal_places=2, max_digits=12, default=0)

    def __str__(self):
        return self.user.profile.full_name

    

