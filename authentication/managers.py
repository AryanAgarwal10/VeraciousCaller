from django.contrib.auth.base_user import BaseUserManager
from .utils import isValidEmail, isValidPhoneNumber
class UserManager(BaseUserManager):
    def create_user(self, phone_number, name,password, email=None):
        if not phone_number:
            raise ValueError('Phone number needed')
        if not isValidPhoneNumber(phone_number):
            raise ValueError('Invalid phone number format')
        if not name:
            raise ValueError('Name needed')
        if not password:
            raise ValueError('Password needed')
        if (email and not isValidEmail(email)):
            raise ValueError('Please provide valid email')
            
        user = self.model(
            phone_number=phone_number,
            name=name,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
