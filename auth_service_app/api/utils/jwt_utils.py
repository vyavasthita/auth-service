import jwt
from typing import Any, Dict
from api.dependencies import Config

class JWTUtils:
    @staticmethod
    def generate_auth_token(claims: Dict[str, Any]) -> str:
        """
        Generate a JWT token with the given payload. The payload must include 'exp' (expiration datetime).

        Args:
            claims (Dict[str, Any]): The payload to encode in the JWT. Must include 'exp'.

        Returns:
            str: JWT token as a string.
        """
        return jwt.encode(claims, Config().SECRET_KEY, algorithm=Config().ALGORITHM)

    @staticmethod
    def decode_auth_token(token: str) -> Dict[str, Any]:
        """
        Decode a JWT token and return the claims if valid, else raise jwt exceptions.
        Args:
            token (str): JWT token as a string.
        Returns:
            Dict[str, Any]: Decoded claims.
        Raises:
            jwt.ExpiredSignatureError, jwt.InvalidTokenError, etc.
        """
        return jwt.decode(token, Config().SECRET_KEY, algorithms=[Config().ALGORITHM])