from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pydantic import BaseModel, Field

from src.api.dependencies.config_dependency import Config
from src.api.models import User


class TokenClaims(BaseModel):
    """Typed JWT claims — single source of truth for token payload."""

    sub: str = Field(description="Subject (username)")
    exp: float = Field(description="Expiration time (unix timestamp)")
    iat: float = Field(description="Issued at (unix timestamp)")
    jti: str = Field(description="Unique token ID for revocation")

    @classmethod
    def for_user(cls, user: User) -> "TokenClaims":
        """Factory: build claims from a User entity and config."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=Config().TOKEN_EXPIRE_MINUTES)

        return cls(
            sub=user.username,
            exp=expire.timestamp(),
            iat=now.timestamp(),
            jti=str(uuid4()),
        )

    def to_payload(self) -> dict:
        """Serialize to a JWT-compatible dict."""
        return self.model_dump()
