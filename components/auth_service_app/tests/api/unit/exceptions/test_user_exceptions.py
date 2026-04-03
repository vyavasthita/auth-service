from fastapi import status

from src.api.exceptions import UserAlreadyExistsException, UserNotFoundException


def test_user_already_exists_exception():
    email = "test@example.com"
    exc = UserAlreadyExistsException(email)
    assert exc.email == email
    assert exc.status_code == status.HTTP_409_CONFLICT


def test_user_not_found_exception():
    user_id = "123"
    exc = UserNotFoundException(user_id)
    assert exc.status_code == status.HTTP_404_NOT_FOUND
