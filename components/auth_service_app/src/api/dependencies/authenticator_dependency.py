from jwt_lib.authenticator import UserAuthenticator

from src.api.dependencies.config_dependency import Config


class AuthenticatorProvider:
    """Provides a singleton UserAuthenticator via FastAPI Depends()."""

    def __init__(self) -> None:
        self._authenticator: UserAuthenticator | None = None

    def __call__(self) -> UserAuthenticator:
        if self._authenticator is None:
            self._authenticator = UserAuthenticator(
                issuer=Config().JWT_ISSUER,
                jwks_host=Config().JWKS_HOST,
                audience=Config().JWT_AUDIENCE,
            )
        return self._authenticator


get_authenticator = AuthenticatorProvider()
