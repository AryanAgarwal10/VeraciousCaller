import re
from django.core.validators import validate_email
from django.forms import ValidationError

def isValidPhoneNumber(phone_number):
    pattern = r'^\d{10}$'
    regex = re.compile(pattern)
    return bool(regex.match(str(phone_number)))

def isValidEmail(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True