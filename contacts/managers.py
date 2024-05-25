from authentication.utils import isValidPhoneNumber
from django.db import models

class ContactManager(models.Manager):
    def create_contact(self,owner,phone_number,name):
        if not phone_number:
            raise ValueError('Phone number needed')
        if not isValidPhoneNumber(phone_number):
            raise ValueError('Invalid phone number format')
        if not name:
            raise ValueError('Name needed')
        
        contact=self.model(
            owner=owner,
            phone_number=phone_number,
            name=name
        )
        contact.save(using=self._db)
        return contact