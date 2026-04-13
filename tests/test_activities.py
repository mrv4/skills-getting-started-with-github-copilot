"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_success(self, client_with_reset):
        """
        Test that GET /activities returns all activities with correct structure.

        AAA Pattern:
        - Arrange: client is ready
        - Act: fetch all activities
        - Assert: response contains all activities with expected fields
        """
        # Act
        response = client_with_reset.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

        # Verify structure of each activity
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_get_activities_contains_chess_club(self, client_with_reset):
        """
        Test that Chess Club is in the activities list.

        AAA Pattern:
        - Arrange: client is ready
        - Act: fetch all activities
        - Assert: Chess Club exists with correct details
        """
        # Act
        response = client_with_reset.get("/activities")
        activities = response.json()

        # Assert
        assert "Chess Club" in activities
        chess = activities["Chess Club"]
        assert chess["max_participants"] == 12
        assert len(chess["participants"]) >= 0

    def test_get_activities_participants_list_format(self, client_with_reset):
        """
        Test that participants are returned as a list of email strings.

        AAA Pattern:
        - Arrange: client is ready
        - Act: fetch activities
        - Assert: participants list contains valid email strings
        """
        # Act
        response = client_with_reset.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_details in activities.items():
            participants = activity_details["participants"]
            assert isinstance(participants, list)
            for participant in participants:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
