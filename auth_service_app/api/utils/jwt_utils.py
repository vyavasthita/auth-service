import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict


# Secret key for JWT encoding (should be kept secure in env/config)
SECRET_KEY = "auth-service-secret"  # Replace with env/config in production
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

class JWTUtils:
    @staticmethod
    def generate_auth_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
        """
        Generate a JWT token with the given payload and expiration.

        Args:
            data (Dict[str, Any]): The payload to encode in the JWT (e.g., {"sub": user_id})
            expires_delta (timedelta, optional): Optional timedelta for token expiration.

        Returns:
            str: JWT token as a string.
        """
        """
        Generate a JWT token with the given payload and expiration.
        Args:
            data: The payload to encode in the JWT (e.g., {"sub": user_id})
            expires_delta: Optional timedelta for token expiration
        Returns:
            JWT token as a string
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
