import hashlib
import logging
import os
from base64 import urlsafe_b64encode
from pathlib import Path

from jwt.algorithms import RSAAlgorithm

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src.api.dependencies import Config


logger = logging.getLogger(__name__)


class KeyManager:
    """Manages RSA key pair for JWT signing and JWKS endpoint."""

    _instance: "KeyManager | None" = None

    def __new__(cls) -> "KeyManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        self._private_key_path = Path(Config().RSA_PRIVATE_KEY_FILE)
        self._public_key_path = Path(Config().RSA_PUBLIC_KEY_FILE)
        self._private_key, self._public_key = self._load_or_generate_keys()
        self._kid = self._compute_kid()

        logger.info(f"KeyManager initialized with kid={self._kid}")

    def _load_or_generate_keys(self):
        if self._private_key_path.exists() and self._public_key_path.exists():
            logger.info("Loading existing RSA key pair from disk.")
            private_key = serialization.load_pem_private_key(
                self._private_key_path.read_bytes(),
                password=None,
            )
            public_key = serialization.load_pem_public_key(
                self._public_key_path.read_bytes(),
            )
            return private_key, public_key

        logger.info("Generating new RSA key pair.")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        self._private_key_path.parent.mkdir(parents=True, exist_ok=True)

        self._private_key_path.write_bytes(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        os.chmod(self._private_key_path, 0o600)

        self._public_key_path.write_bytes(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

        logger.info(f"RSA key pair saved to {self._private_key_path.parent}")
        return private_key, public_key

    def _compute_kid(self) -> str:
        """Compute a stable key ID from the public key DER encoding."""
        der = self._public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        digest = hashlib.sha256(der).digest()
        return urlsafe_b64encode(digest[:16]).decode().rstrip("=")

    @property
    def private_key(self):
        return self._private_key

    @property
    def public_key(self):
        return self._public_key

    @property
    def kid(self) -> str:
        return self._kid

    def get_jwks(self) -> dict:
        """Return the public key in JWKS format."""
        

        jwk_dict = RSAAlgorithm.to_jwk(self._public_key, as_dict=True)
        jwk_dict["kid"] = self._kid
        jwk_dict["use"] = "sig"
        jwk_dict["alg"] = "RS256"

        return {"keys": [jwk_dict]}
