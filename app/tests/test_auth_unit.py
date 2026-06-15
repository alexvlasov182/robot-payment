"""Unit tests for authentication"""

import pytest
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService


class TestAuthService:
    """Test AuthService class"""

    def test_register_user_success(self, db_session: Session):
        service = AuthService(db_session)
        result = service.register_user("new@test.com", "password123")
        assert "id" in result
        assert result["email"] == "new@test.com"

    def test_register_user_email_already_exists(self, db_session: Session, test_user):
        service = AuthService(db_session)
        with pytest.raises(ValueError, match="Email already registered"):
            service.register_user(test_user.email, "password123")

    def test_authenticate_user_success(self, db_session: Session, test_user):
        service = AuthService(db_session)
        result = service.authenticate_user(test_user.email, "testpassword123")
        assert result["email"] == test_user.email

    def test_authenticate_user_wrong_password(self, db_session: Session, test_user):
        service = AuthService(db_session)
        with pytest.raises(ValueError, match="Invalid credentials"):
            service.authenticate_user(test_user.email, "wrongpassword")

    def test_authenticate_user_user_not_found(self, db_session: Session):
        service = AuthService(db_session)
        with pytest.raises(ValueError, match="Invalid credentials"):
            service.authenticate_user("nonexistent@test.com", "password123")

    def test_refresh_token_invalid(self, db_session: Session):
        service = AuthService(db_session)
        with pytest.raises(ValueError, match="Invalid refresh token"):
            service.refresh_token("invalid-token")

    def test_logout_success(self, db_session: Session):
        service = AuthService(db_session)
        result = service.logout("some-token")
        assert result is True
