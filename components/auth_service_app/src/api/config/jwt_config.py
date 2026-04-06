from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    """JWT authentication settings."""

    SECRET_KEY: str = "auth-service-secret"
    ALGORITHM: str = "RS256"
    TOKEN_EXPIRE_MINUTES: int = 10

    # RSA key file paths (auto-generated in dev if missing)
    RSA_PRIVATE_KEY_FILE: str = "/app/keys/private.pem"
    RSA_PUBLIC_KEY_FILE: str = "/app/keys/public.pem"

    # Token claims
    JWT_ISSUER: str = "auth-service"
    JWT_AUDIENCE: str = "auth-service"

    # JWKS host for token-validator (points to self for self-validation)
    JWKS_HOST: str = "http://localhost:2002/auth-service"
