from django.db import models
from django.utils import timezone

from authentication.models import User
from contacts.managers import ContactManager

class Contact(models.Model):
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects=ContactManager()

    def __str__(self):
        return self.name