from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validate_email_def(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
