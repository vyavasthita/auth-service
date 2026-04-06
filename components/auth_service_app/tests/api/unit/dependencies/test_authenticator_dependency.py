from unittest.mock import MagicMock, patch


def test_authenticator_provider_returns_authenticator():
    """AuthenticatorProvider creates a UserAuthenticator on first call."""
    with patch("src.api.dependencies.authenticator_dependency.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.JWT_ISSUER = "auth-service"
        mock_config.JWKS_HOST = "http://localhost:5002/auth-service"
        mock_config.JWT_AUDIENCE = "auth-service"

        with patch("src.api.dependencies.authenticator_dependency.UserAuthenticator") as mock_auth_cls:
            mock_authenticator = MagicMock()
            mock_auth_cls.return_value = mock_authenticator

            from src.api.dependencies.authenticator_dependency import AuthenticatorProvider

            provider = AuthenticatorProvider()
            result = provider()

            assert result is mock_authenticator
            mock_auth_cls.assert_called_once_with(
                issuer="auth-service",
                jwks_host="http://localhost:5002/auth-service",
                audience="auth-service",
            )


def test_authenticator_provider_returns_same_instance():
    """Repeated calls return the same cached UserAuthenticator instance."""
    with patch("src.api.dependencies.authenticator_dependency.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.JWT_ISSUER = "auth-service"
        mock_config.JWKS_HOST = "http://localhost:5002/auth-service"
        mock_config.JWT_AUDIENCE = "auth-service"

        with patch("src.api.dependencies.authenticator_dependency.UserAuthenticator") as mock_auth_cls:
            mock_auth_cls.return_value = MagicMock()

            from src.api.dependencies.authenticator_dependency import AuthenticatorProvider

            provider = AuthenticatorProvider()
            first = provider()
            second = provider()

            assert first is second
            assert mock_auth_cls.call_count == 1
