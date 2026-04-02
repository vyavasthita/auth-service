import jwt
from typing import Any, Dict
from src.api.dependencies.config_dependency import Config


class JWTUtils:
    @staticmethod
    def generate_auth_token(claims: Dict[str, Any]) -> str:
        """Generate a JWT token with the given payload."""
        return jwt.encode(claims, Config().SECRET_KEY, algorithm=Config().ALGORITHM)

    @staticmethod
    def decode_auth_token(token: str) -> Dict[str, Any]:
        """Decode a JWT token and return the claims if valid."""
        return jwt.decode(token, Config().SECRET_KEY, algorithms=[Config().ALGORITHM])
