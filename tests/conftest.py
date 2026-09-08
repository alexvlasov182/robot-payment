"""Pytest configuration for tests."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.robot import Robot, RobotType
from app.models.user import User

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-ci-only"
os.environ["APP_ENV"] = "testing"


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Create clean database for every test.
    """

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for a test."""
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


session = db_session


@pytest.fixture(scope="function")
def client(db_session: Session):
    """Create a TestClient with overridden get_db dependency."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user in the database."""
    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def test_robot(db_session: Session):
    """Create a test robot in the database."""
    robot = Robot(
        name="Test Robot T4",
        robot_type=RobotType.T4,
        serial_number="TEST-001",
        status="offline",
        capabilities={
            "tap": True,
            "chip": True,
        },
    )

    db_session.add(robot)
    db_session.commit()
    db_session.refresh(robot)

    return robot


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for a test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "testpassword123",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
