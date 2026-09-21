from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
