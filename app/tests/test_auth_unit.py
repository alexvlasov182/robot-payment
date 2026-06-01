"""Unit tests for Auth"""

from unittest.mock import MagicMock, patch

import pytest

from app.services.auth_service import AuthService


def test_register_user_success():
    """Register a new user with valid data"""
    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    service.user_repo.exists_by_email = MagicMock(return_value=False)

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "test@example.com"
    service.user_repo.create = MagicMock(return_value=fake_user)

    result = service.register_user("test@example.com", "test123")

    assert result["email"] == "test@example.com"


def test_register_user_email_already_exists():
    """Register fails if email is already taken"""
    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    service.user_repo.exists_by_email = MagicMock(return_value=True)

    with pytest.raises(ValueError):
        service.register_user("test@example.com", "test123")


def test_authenticate_user_success():
    """Authenticate returns user data for valid credentials"""
    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "test@example.com"
    fake_user.hashed_password = "somehash"

    service.user_repo.get_by_email = MagicMock(return_value=fake_user)

    with patch("app.services.auth_service.verify_password", return_value=True):
        result = service.authenticate_user("test@example.com", "test123")

    # Should return user dict, not tokens
    assert result["id"] == 1
    assert result["email"] == "test@example.com"
    assert "access_token" not in result


def test_authenticate_user_wrong_password():
    """Authentication fails if password is wrong"""

    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "test@example.com"
    fake_user.hashed_password = "somehashtedpassword"
    service.user_repo.create = MagicMock(return_value=fake_user)

    with patch("app.services.auth_service.verify_password", return_value=False):
        with pytest.raises(ValueError):
            service.authenticate_user("test@example.com", "wrongpassword")


def test_authenticate_user_user_not_found():
    """Authentication fails if email was never registered"""

    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    service.user_repo.get_by_email = MagicMock(return_value=None)

    with pytest.raises(ValueError):
        service.authenticate_user("ghost@example.com", "test123")


def test_refresh_token_invalid():
    """Refresh fails if token is invalid"""
    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    # Patch the actual function where it's defined
    with patch("app.core.security.decode_refresh_token", return_value=None):
        with pytest.raises(ValueError, match="Invalid refresh token"):
            service.refresh_token("invalid_token")


def test_logout_success():
    """Logout clears refresh token from database"""

    mock_db = MagicMock()
    service = AuthService(db=mock_db)

    service.logout("test@example.com")
