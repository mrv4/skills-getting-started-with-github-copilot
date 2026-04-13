"""
Pytest configuration and shared fixtures for API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient for making requests to the app.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture to reset the in-memory activities database before each test.
    This ensures test isolation and prevents cross-test contamination.
    """
    # Store original state
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy(),
        }
        for key, value in activities.items()
    }

    yield

    # Reset activities to original state after test
    activities.clear()
    for key, value in original_activities.items():
        activities[key] = value


@pytest.fixture
def client_with_reset(client, reset_activities):
    """
    Combine client and reset_activities fixtures for convenience.
    Use this fixture in tests that need both a test client and activity reset.
    """
    return client
