from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pydantic import BaseModel, Field

from src.api.dependencies.config_dependency import Config


class TokenClaims(BaseModel):
    """Typed JWT claims — single source of truth for token payload."""

    sub: str = Field(description="Subject (user ID)")
    username: str = Field(description="Username")
    exp: float = Field(description="Expiration time (unix timestamp)")
    iat: float = Field(description="Issued at (unix timestamp)")
    nbf: float = Field(description="Not before (unix timestamp)")
    jti: str = Field(description="Unique token ID for revocation")
    iss: str = Field(description="Token issuer")
    aud: str = Field(description="Token audience")
    tokenType: str = Field(default="UserAuthToken", description="Token type")  # noqa: N815
    principalType: str = Field(default="USER", description="Principal type")  # noqa: N815
    connectionMethod: str = Field(default="UIDPWD", description="Connection method")  # noqa: N815
    roles: list[str] = Field(default_factory=list, description="User roles")

    @classmethod
    def for_user(cls, user_id: str, username: str, user_roles: list[str]) -> "TokenClaims":
        """Factory: build claims from a User entity and config."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=Config().TOKEN_EXPIRE_MINUTES)

        return cls(
            sub=user_id,
            username=username,
            roles=user_roles,
            exp=expire.timestamp(),
            iat=now.timestamp(),
            nbf=now.timestamp(),
            jti=str(uuid4()),
            iss=Config().JWT_ISSUER,
            aud=Config().JWT_AUDIENCE,
        )

    def to_payload(self) -> dict:
        """Serialize to a JWT-compatible dict."""
        return self.model_dump()
