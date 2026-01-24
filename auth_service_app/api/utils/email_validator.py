from functools import wraps
from email_validator import validate_email, EmailNotValidError
from api.exceptions import EmailFormatException


def email_format_validator(func):
    @wraps(func)
    async def wrapper(self, db_session, email, *args, **kwargs):
        # Only check email format, assume presence/type checked by Pydantic
        try:
            email_obj = validate_email(email)
            normalized_email = email_obj.email
        except EmailNotValidError as e:
            raise EmailFormatException(email=email)
        return await func(self, db_session, normalized_email, *args, **kwargs)
    return wrapper
