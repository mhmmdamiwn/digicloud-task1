import pytest
from service import AuthService  

@pytest.fixture
def auth_service():
    return AuthService()

def test_register_user(auth_service):
    result = auth_service.register_user("test_user", "password123")
    assert result is True  

def test_register_existing_user(auth_service):
    auth_service.register_user("existing_user", "password123")
    result = auth_service.register_user("existing_user", "password456")
    assert result is False 

def test_login_success(auth_service):
    auth_service.register_user("login_user", "password123")
    result = auth_service.login("login_user", "password123")
    assert result is not None  

def test_login_failure(auth_service):
    result = auth_service.login("unknown_user", "password123")
    assert result is None  

def test_validate_token_success(auth_service):
    token = auth_service.generate_token("valid_user")
    assert auth_service.validate_token(token) is True

def test_validate_token_failure(auth_service):
    assert auth_service.validate_token("invalid_token") is False
