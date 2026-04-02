import inspect
from functools import wraps
from email_validator import validate_email, EmailNotValidError
from src.api.exceptions import EmailFormatException


def email_format_validator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """Validates the email argument and normalizes it."""
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        if 'email' in bound.arguments:
            email = bound.arguments['email']

            try:
                email_obj = validate_email(email)
                normalized_email = email_obj.email
            except EmailNotValidError as e:
                raise EmailFormatException(str(e))
            bound.arguments['email'] = normalized_email

        return await func(*bound.args, **bound.kwargs)

    return wrapper
