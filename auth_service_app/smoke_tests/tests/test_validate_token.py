import requests
import os

def test_validate_token_smoke():
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    # Register and login to get a token
    register_resp = requests.post(f"{base_url}/register", json={
        "email": "smokeuser@example.com",
        "name": "Smoke User",
        "password": "smokepass123",
        "phone_number": "1234567890"
    })
    # Ignore if already registered
    login_resp = requests.post(f"{base_url}/login", json={
        "email": "smokeuser@example.com",
        "password": "smokepass123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    # Validate token
    validate_resp = requests.post(f"{base_url}/validate-token", json={"token": token})
    assert validate_resp.status_code == 200
    data = validate_resp.json()
    assert data["is_valid"] is True
    assert data["user_id"] == "smokeuser@example.com"
    assert data["message"] == "Token is valid."
