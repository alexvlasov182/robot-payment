"""Integration tests for user data isolation (multi-tenant ownership)."""

from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str, password: str = "Test123!") -> dict:
    """Register a user and return auth headers with their access token."""
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestRobotIsolation:
    """Ensure one user can never see or modify another user's robots."""

    def test_user_cannot_get_another_users_robot(self, client: TestClient):
        """User B requesting User A's robot by ID must get 404, not the data."""
        alex_headers = _register_and_login(client, "alex_isolation@test.com")
        john_headers = _register_and_login(client, "john_isolation@test.com")

        create = client.post(
            "/api/v1/robots/",
            headers=alex_headers,
            json={
                "name": "Alex Robot",
                "serial_number": "ISO-001",
                "robot_type": "T1",
                "capabilities": {"tap": True},
            },
        )
        assert create.status_code == 201
        robot_id = create.json()["id"]

        # John tries to fetch Alex's robot directly by ID
        response = client.get(f"/api/v1/robots/{robot_id}", headers=john_headers)
        assert response.status_code == 404

    def test_user_list_only_shows_own_robots(self, client: TestClient):
        """GET /robots/ must never leak another user's robots into the list."""
        alex_headers = _register_and_login(client, "alex_list@test.com")
        john_headers = _register_and_login(client, "john_list@test.com")

        client.post(
            "/api/v1/robots/",
            headers=alex_headers,
            json={
                "name": "Alex Robot 2",
                "serial_number": "ISO-002",
                "robot_type": "T1",
                "capabilities": {"tap": True},
            },
        )

        # John's list must be empty - he hasn't created any robots
        john_list = client.get("/api/v1/robots/", headers=john_headers)
        assert john_list.status_code == 200
        assert john_list.json() == []

        # Alex's list must contain exactly his own robot
        alex_list = client.get("/api/v1/robots/", headers=alex_headers)
        assert alex_list.status_code == 200
        serials = [r["serial_number"] for r in alex_list.json()]
        assert "ISO-002" in serials

    def test_user_cannot_delete_another_users_robot(self, client: TestClient):
        """DELETE on a robot owned by another user must return 404, and the robot must survive."""
        alex_headers = _register_and_login(client, "alex_delete@test.com")
        john_headers = _register_and_login(client, "john_delete@test.com")

        create = client.post(
            "/api/v1/robots/",
            headers=alex_headers,
            json={
                "name": "Alex Robot 3",
                "serial_number": "ISO-003",
                "robot_type": "T1",
                "capabilities": {"tap": True},
            },
        )
        robot_id = create.json()["id"]

        delete_attempt = client.delete(f"/api/v1/robots/{robot_id}", headers=john_headers)
        assert delete_attempt.status_code == 404

        # Confirm the robot is untouched from the real owner's perspective
        still_there = client.get(f"/api/v1/robots/{robot_id}", headers=alex_headers)
        assert still_there.status_code == 200
