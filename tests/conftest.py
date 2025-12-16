"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app import create_app


@pytest.fixture
def app():
    """Create application instance for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return TestClient(app)
