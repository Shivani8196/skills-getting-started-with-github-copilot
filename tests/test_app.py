import pytest

# Arrange-Act-Assert pattern is used in all tests

def test_get_activities(client):
    # Arrange: client fixture is provided
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act: Sign up
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Act: Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert unregister_resp.status_code == 200
    assert f"has been removed" in unregister_resp.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    email = "emma@mergington.edu"  # Already in Programming Class
    activity = "Programming Class"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_unregister_not_registered(client):
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert "not registered" in resp.json()["detail"]
