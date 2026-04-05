def test_get_activities_returns_expected_structure(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 9

    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity in payload.items():
        assert activity_name
        assert required_fields.issubset(activity.keys())
        assert isinstance(activity["participants"], list)
