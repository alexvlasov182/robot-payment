"""Unit tests for authentication"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.security import create_access_token


class TestAuthService:
    """Test AuthService class"""

    def test_register_user_success(self, db: Session):
        """Test successful user registration"""
        service = AuthService(db)
        result = service.register_user("new@test.com", "password123")
        
        assert "id" in result
        assert result["email"] == "new@test.com"

    def test_register_user_email_already_exists(self, db: Session, test_user):
        """Test registration with existing email"""
        service = AuthService(db)
        
        with pytest.raises(ValueError, match="Email already registered"):
            service.register_user(test_user.email, "password123")

    def test_authenticate_user_success(self, db: Session, test_user):
        """Test successful authentication"""
        service = AuthService(db)
        result = service.authenticate_user(test_user.email, "testpassword123")
        
        assert result["email"] == test_user.email

    def test_authenticate_user_wrong_password(self, db: Session, test_user):
        """Test authentication with wrong password"""
        service = AuthService(db)
        
        with pytest.raises(ValueError, match="Invalid credentials"):
            service.authenticate_user(test_user.email, "wrongpassword")

    def test_authenticate_user_user_not_found(self, db: Session):
        """Test authentication with non-existent user"""
        service = AuthService(db)
        
        with pytest.raises(ValueError, match="Invalid credentials"):
            service.authenticate_user("nonexistent@test.com", "password123")

    def test_refresh_token_invalid(self, db: Session):
        """Test refresh token with invalid token"""
        service = AuthService(db)
        
        with pytest.raises(ValueError, match="Invalid refresh token"):
            service.refresh_token("invalid-token")

    def test_logout_success(self, db: Session):
        """Test logout functionality"""
        service = AuthService(db)
        result = service.logout("some-token")
        
        assert result is True
