"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.
"""

import pytest


class TestDeleteParticipant:
    """Test suite for participant removal functionality."""

    def test_delete_participant_success(self, client_with_reset):
        """
        Test successful participant removal from activity.

        AAA Pattern:
        - Arrange: sign up a participant first
        - Act: delete the participant
        - Assert: participant is removed and response confirms success
        """
        # Arrange
        test_email = "remove@mergington.edu"
        activity = "Drama Club"
        client_with_reset.post(f"/activities/{activity}/signup", params={"email": test_email})

        # Act
        response = client_with_reset.delete(
            f"/activities/{activity}/participants",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert test_email in result["message"]

        # Verify participant was removed
        activities_response = client_with_reset.get("/activities")
        activities = activities_response.json()
        assert test_email not in activities[activity]["participants"]

    def test_delete_nonexistent_participant_fails(self, client_with_reset):
        """
        Test that deleting a participant not in activity returns 404 error.

        AAA Pattern:
        - Arrange: prepare email that is not signed up
        - Act: attempt to delete non-existent participant
        - Assert: response is 404 with error detail
        """
        # Arrange
        test_email = "notregistered@mergington.edu"
        activity = "Art Studio"

        # Act
        response = client_with_reset.delete(
            f"/activities/{activity}/participants",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_delete_from_nonexistent_activity_fails(self, client_with_reset):
        """
        Test that deleting from non-existent activity returns 404 error.

        AAA Pattern:
        - Arrange: prepare invalid activity name
        - Act: attempt delete from non-existent activity
        - Assert: response is 404 with error detail
        """
        # Arrange
        test_email = "test@mergington.edu"
        fake_activity = "Fake Activity"

        # Act
        response = client_with_reset.delete(
            f"/activities/{fake_activity}/participants",
            params={"email": test_email},
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_delete_participant_preserves_others(self, client_with_reset):
        """
        Test that deleting one participant doesn't affect others.

        AAA Pattern:
        - Arrange: sign up two participants for same activity
        - Act: delete the first participant
        - Assert: second participant remains, first is removed
        """
        # Arrange
        email1 = "keep@mergington.edu"
        email2 = "remove@mergington.edu"
        activity = "Debate Team"
        client_with_reset.post(f"/activities/{activity}/signup", params={"email": email1})
        client_with_reset.post(f"/activities/{activity}/signup", params={"email": email2})

        # Act
        response = client_with_reset.delete(
            f"/activities/{activity}/participants",
            params={"email": email2},
        )

        # Assert
        assert response.status_code == 200

        # Verify correct participant was removed
        activities_response = client_with_reset.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity]["participants"]
        assert email2 not in activities[activity]["participants"]

    def test_delete_then_can_signup_again(self, client_with_reset):
        """
        Test that a participant can sign up again after being removed.

        AAA Pattern:
        - Arrange: sign up a participant
        - Act: delete participant, then sign up again
        - Assert: participant is back in the activity
        """
        # Arrange
        test_email = "rejoin@mergington.edu"
        activity = "Science Club"
        client_with_reset.post(f"/activities/{activity}/signup", params={"email": test_email})

        # Act
        client_with_reset.delete(f"/activities/{activity}/participants", params={"email": test_email})
        signup_response = client_with_reset.post(
            f"/activities/{activity}/signup", params={"email": test_email}
        )

        # Assert
        assert signup_response.status_code == 200

        # Verify participant is back
        activities_response = client_with_reset.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity]["participants"]
