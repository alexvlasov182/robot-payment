"""Pytest configuration for tests"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-ci-only"
os.environ["APP_ENV"] = "testing"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.models.user import User
from app.models.robot import Robot, RobotType

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables once for the whole test session"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Session:  # type: ignore
    """
    Each test gets a clean session, rolled back after.
    No more db + db_session alias confusion.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session  # type: ignore

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:  # type: ignore
    """Test client that uses the test database session"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client  # type: ignore

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session):  # type: ignore
    """Create a test user in the database"""
    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_robot(db_session: Session):
    """Create a test robot in the database"""
    robot = Robot(
        name="Test Robot T4",
        robot_type=RobotType.T4,
        serial_number="TEST-001",
        status="offline",
        capabilities="tap,chip,swipe",
    )
    db_session.add(robot)
    db_session.commit()
    db_session.refresh(robot)
    return robot


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user):  # type: ignore
    """Get auth headers for protected endpoints"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user.email, "password": "testpassword123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
