import pytest


@pytest.mark.xfail(reason="Capacity validation is not implemented in backend yet.")
def test_signup_fails_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Fill to max capacity (12)
    for i in range(10):
        client.post(f"/activities/{activity_name}/signup", params={"email": f"full{i}@mergington.edu"})

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"}
    )

    # Assert
    assert initial_count == 2
    assert response.status_code == 400


def test_signup_succeeds_for_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
