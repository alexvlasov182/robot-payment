"""Integration tests for complete API flows"""

from fastapi.testclient import TestClient


class TestAuthIntegration:
    """Test complete authentication flow"""

    def test_full_auth_flow(self, client: TestClient):
        """Test register -> login -> access protected endpoint"""

        # 1. Register
        register = client.post(
            "/api/v1/auth/register",
            json={
                "email": "integration@test.com",
                "password": "Test123!",
                "confirm_password": "Test123!",
            },
        )
        assert register.status_code == 201

        # 2. Login
        login = client.post(
            "/api/v1/auth/login",
            json={"email": "integration@test.com", "password": "Test123!"},
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        assert token is not None

        # 3. Access protected endpoint with token
        robots = client.get(
            "/api/v1/robots/", headers={"Authorization": f"Bearer {token}"}
        )
        assert robots.status_code == 200

        return token

    def test_cannot_access_protected_without_token(self, client: TestClient):
        """Test protected endpoint without token returns 401"""
        response = client.get("/api/v1/robots/")
        assert response.status_code == 401


class TestRobotIntegration:
    """Test complete robot management flow"""

    def test_full_robot_lifecycle(self, client: TestClient):
        """Test create -> read -> update -> delete robot"""

        # First, create user and get token
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "robotflow@test.com",
                "password": "Test123!",
                "confirm_password": "Test123!",
            },
        )
        login = client.post(
            "/api/v1/auth/login",
            json={"email": "robotflow@test.com", "password": "Test123!"},
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. CREATE robot
        create = client.post(
            "/api/v1/robots/",
            headers=headers,
            json={
                "name": "Integration Robot",
                "serial_number": "INT-001",
                "robot_type": "T4",
                "capabilities": "tap,chip",
            },
        )
        assert create.status_code == 201
        robot_id = create.json()["id"]

        # 2. READ robot
        read = client.get(f"/api/v1/robots/{robot_id}", headers=headers)
        assert read.status_code == 200
        assert read.json()["name"] == "Integration Robot"

        # 3. UPDATE status - using query parameter, NOT JSON body
        update = client.patch(
            f"/api/v1/robots/{robot_id}/status?status=online", headers=headers
        )
        assert update.status_code == 200
        assert update.json()["status"] == "online"

        # 4. DELETE robot
        delete = client.delete(f"/api/v1/robots/{robot_id}", headers=headers)
        assert delete.status_code == 204

        # 5. Verify deleted
        get_deleted = client.get(f"/api/v1/robots/{robot_id}", headers=headers)
        assert get_deleted.status_code == 404


class TestTerminalIntegration:
    """Test terminal endpoints"""

    def test_terminal_endpoints(self, client: TestClient):
        """Test all terminal endpoints work"""

        # McDonald's
        mcd = client.get("/api/v1/terminals/mcdonalds")
        assert mcd.status_code == 200
        assert mcd.json()["merchant"] == "McDonald's"

        # Grocery regression
        grocery = client.get("/api/v1/terminals/grocery/regression")
        assert grocery.status_code == 200
        assert grocery.json()["merchant"] == "Migros"

        # Payment simulation
        payment = client.post(
            "/api/v1/terminals/test",
            json={"terminal_id": 999, "amount": 42.50, "payment_method": "tap"},
        )
        assert payment.status_code == 200
        assert payment.json()["status"] == "approved"
