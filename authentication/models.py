from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from authentication.managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser):
    phone_number = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone_number
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
