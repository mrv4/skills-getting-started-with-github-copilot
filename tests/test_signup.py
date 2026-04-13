"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupForActivity:
    """Test suite for activity signup functionality."""

    def test_signup_success(self, client_with_reset):
        """
        Test successful signup adds participant to activity.

        AAA Pattern:
        - Arrange: prepare test email and activity
        - Act: send signup request
        - Assert: participant is added and response confirms success
        """
        # Arrange
        test_email = "test@mergington.edu"
        activity = "Programming Class"

        # Act
        response = client_with_reset.post(
            f"/activities/{activity}/signup",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert test_email in result["message"]
        assert activity in result["message"]

        # Verify participant was added
        activities_response = client_with_reset.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity]["participants"]

    def test_signup_duplicate_email_fails(self, client_with_reset):
        """
        Test that duplicate signup is rejected with 400 error.

        AAA Pattern:
        - Arrange: sign up a participant once
        - Act: attempt to sign up the same email again
        - Assert: second signup returns 400 error
        """
        # Arrange
        test_email = "duplicate@mergington.edu"
        activity = "Chess Club"
        client_with_reset.post(f"/activities/{activity}/signup", params={"email": test_email})

        # Act
        response = client_with_reset.post(
            f"/activities/{activity}/signup",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"].lower() or "Student already" in result["detail"]

    def test_signup_nonexistent_activity_fails(self, client_with_reset):
        """
        Test that signup to non-existent activity returns 404 error.

        AAA Pattern:
        - Arrange: prepare invalid activity name
        - Act: attempt signup for non-existent activity
        - Assert: response is 404 with error detail
        """
        # Arrange
        test_email = "test@mergington.edu"
        fake_activity = "Nonexistent Activity"

        # Act
        response = client_with_reset.post(
            f"/activities/{fake_activity}/signup",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_signup_multiple_participants(self, client_with_reset):
        """
        Test that multiple different emails can sign up for same activity.

        AAA Pattern:
        - Arrange: prepare two different emails
        - Act: sign up both emails for the same activity
        - Assert: both participants are in the activity's participant list
        """
        # Arrange
        email1 = "user1@mergington.edu"
        email2 = "user2@mergington.edu"
        activity = "Tennis Club"

        # Act
        response1 = client_with_reset.post(f"/activities/{activity}/signup", params={"email": email1})
        response2 = client_with_reset.post(f"/activities/{activity}/signup", params={"email": email2})

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both are added
        activities_response = client_with_reset.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity]["participants"]
        assert email2 in activities[activity]["participants"]
