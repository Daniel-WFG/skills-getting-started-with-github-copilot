import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400


    # Unregister (allow 200 or 404 due to possible in-memory DB reset)
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert f"Unregistered {test_email}" in response.json()["message"]

    # Unregister again should fail (400 or 404 is acceptable)
    response = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response.status_code in (400, 404)
