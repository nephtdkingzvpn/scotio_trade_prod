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
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

