from unittest.mock import patch


def test_token_claims_for_user_contains_required_fields():
    """TokenClaims.for_user produces all fields needed by token-validator."""
    with patch("src.utils.token_claims.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.TOKEN_EXPIRE_MINUTES = 10
        mock_config.JWT_ISSUER = "auth-service"
        mock_config.JWT_AUDIENCE = "auth-service"

        from src.utils.token_claims import TokenClaims

        claims = TokenClaims.for_user(user_id="abc-123", username="testuser", user_roles=["user"])

    assert claims.sub == "abc-123"
    assert claims.username == "testuser"
    assert claims.iss == "auth-service"
    assert claims.aud == "auth-service"
    assert claims.tokenType == "UserAuthToken"
    assert claims.principalType == "USER"
    assert claims.connectionMethod == "UIDPWD"
    assert claims.roles == ["user"]
    assert claims.jti  # non-empty
    assert claims.nbf <= claims.iat
    assert claims.exp > claims.iat


def test_token_claims_expiry_matches_config():
    """exp should be iat + TOKEN_EXPIRE_MINUTES."""
    with patch("src.utils.token_claims.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.TOKEN_EXPIRE_MINUTES = 15
        mock_config.JWT_ISSUER = "test-issuer"
        mock_config.JWT_AUDIENCE = "test-audience"

        from src.utils.token_claims import TokenClaims

        claims = TokenClaims.for_user(user_id="abc-123", username="testuser", user_roles=["user"])

    expected_delta = 15 * 60
    actual_delta = claims.exp - claims.iat
    assert abs(actual_delta - expected_delta) < 2  # allow 2s clock drift


def test_token_claims_to_payload_returns_dict():
    """to_payload returns a dict with all fields."""
    with patch("src.utils.token_claims.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.TOKEN_EXPIRE_MINUTES = 10
        mock_config.JWT_ISSUER = "auth-service"
        mock_config.JWT_AUDIENCE = "auth-service"

        from src.utils.token_claims import TokenClaims

        claims = TokenClaims.for_user(user_id="abc-123", username="testuser", user_roles=["user"])

    payload = claims.to_payload()

    assert isinstance(payload, dict)
    expected_keys = {
        "sub",
        "username",
        "exp",
        "iat",
        "nbf",
        "jti",
        "iss",
        "aud",
        "tokenType",
        "principalType",
        "connectionMethod",
        "roles",
    }
    assert expected_keys == set(payload.keys())


def test_token_claims_jti_is_unique():
    """Each call to for_user generates a unique jti."""
    with patch("src.utils.token_claims.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.TOKEN_EXPIRE_MINUTES = 10
        mock_config.JWT_ISSUER = "auth-service"
        mock_config.JWT_AUDIENCE = "auth-service"

        from src.utils.token_claims import TokenClaims

        claims1 = TokenClaims.for_user(user_id="abc-123", username="testuser", user_roles=["user"])
        claims2 = TokenClaims.for_user(user_id="abc-123", username="testuser", user_roles=["user"])

    assert claims1.jti != claims2.jti
