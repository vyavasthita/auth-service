from typing import Any

import jwt

from src.utils.key_manager import KeyManager


class JWTUtils:
    @staticmethod
    def generate_auth_token(claims: dict[str, Any]) -> str:
        """Generate a JWT token signed with RS256."""
        key_manager = KeyManager()
        return jwt.encode(
            claims,
            key_manager.private_key,
            algorithm="RS256",
            headers={"kid": key_manager.kid, "typ": "JWT"},
        )

    @staticmethod
    def decode_auth_token(token: str) -> dict[str, Any]:
        """Decode a JWT token using the local RSA public key."""
        key_manager = KeyManager()
        return jwt.decode(
            token,
            key_manager.public_key,
            algorithms=["RS256"],
        )
