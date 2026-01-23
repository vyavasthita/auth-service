import secrets

def generate_auth_token() -> str:
    """Generate a secure random authentication token."""
    return secrets.token_urlsafe(32)
