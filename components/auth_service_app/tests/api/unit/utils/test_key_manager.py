import hashlib
from base64 import urlsafe_b64encode
from unittest.mock import patch

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(autouse=True)
def reset_key_manager_singleton():
    """Reset the KeyManager singleton before each test."""
    from src.utils.key_manager import KeyManager

    KeyManager._instance = None
    yield
    KeyManager._instance = None


@pytest.fixture
def rsa_key_pair(tmp_path):
    """Generate a test RSA key pair and write to temp files."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    priv_path = tmp_path / "private.pem"
    pub_path = tmp_path / "public.pem"

    priv_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    pub_path.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    return priv_path, pub_path, private_key, public_key


def test_key_manager_generates_keys_when_none_exist(tmp_path):
    """KeyManager generates new RSA keys when files don't exist."""
    from src.utils.key_manager import KeyManager

    priv_path = tmp_path / "keys" / "private.pem"
    pub_path = tmp_path / "keys" / "public.pem"

    with (
        patch("src.utils.key_manager.Config") as mock_config_cls,
    ):
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        km = KeyManager()

    assert priv_path.exists()
    assert pub_path.exists()
    assert km.private_key is not None
    assert km.public_key is not None
    assert isinstance(km.kid, str)
    assert len(km.kid) > 0


def test_key_manager_loads_existing_keys(rsa_key_pair):
    """KeyManager loads keys from disk when files already exist."""
    from src.utils.key_manager import KeyManager

    priv_path, pub_path, _, _ = rsa_key_pair

    with patch("src.utils.key_manager.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        km = KeyManager()

    assert km.private_key is not None
    assert km.public_key is not None


def test_key_manager_is_singleton(tmp_path):
    """KeyManager returns the same instance on repeated calls."""
    from src.utils.key_manager import KeyManager

    priv_path = tmp_path / "keys" / "private.pem"
    pub_path = tmp_path / "keys" / "public.pem"

    with patch("src.utils.key_manager.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        km1 = KeyManager()
        km2 = KeyManager()

    assert km1 is km2


def test_key_manager_kid_is_stable(rsa_key_pair):
    """kid is deterministic for the same key."""
    from src.utils.key_manager import KeyManager

    priv_path, pub_path, _, public_key = rsa_key_pair

    with patch("src.utils.key_manager.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        km = KeyManager()

    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    expected_kid = urlsafe_b64encode(hashlib.sha256(der).digest()[:16]).decode().rstrip("=")
    assert km.kid == expected_kid


def test_get_jwks_returns_valid_structure(rsa_key_pair):
    """get_jwks returns a dict with 'keys' containing one JWK."""
    from src.utils.key_manager import KeyManager

    priv_path, pub_path, _, _ = rsa_key_pair

    with patch("src.utils.key_manager.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        km = KeyManager()

    jwks = km.get_jwks()

    assert "keys" in jwks
    assert len(jwks["keys"]) == 1

    jwk = jwks["keys"][0]
    assert jwk["kty"] == "RSA"
    assert jwk["kid"] == km.kid
    assert jwk["use"] == "sig"
    assert jwk["alg"] == "RS256"
    assert "n" in jwk
    assert "e" in jwk


def test_generated_key_file_permissions(tmp_path):
    """Generated private key file should have restricted permissions."""
    import stat

    from src.utils.key_manager import KeyManager

    priv_path = tmp_path / "keys" / "private.pem"
    pub_path = tmp_path / "keys" / "public.pem"

    with patch("src.utils.key_manager.Config") as mock_config_cls:
        mock_config = mock_config_cls.return_value
        mock_config.RSA_PRIVATE_KEY_FILE = str(priv_path)
        mock_config.RSA_PUBLIC_KEY_FILE = str(pub_path)

        KeyManager()

    mode = priv_path.stat().st_mode & 0o777
    assert mode == stat.S_IRUSR | stat.S_IWUSR  # 0o600
