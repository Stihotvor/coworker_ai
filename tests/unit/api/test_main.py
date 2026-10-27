"""Unit tests for API main module."""

from unittest.mock import MagicMock, patch

import pytest

from src.api.main import app


@pytest.fixture
def client():
    """Test client for FastAPI app."""
    from fastapi.testclient import TestClient
    return TestClient(app)


class TestHealthcheckEndpoint:
    """Test cases for healthcheck endpoint."""

    def test_healthcheck_success(self, client):
        """Test healthcheck endpoint returns success."""
        response = client.get("/healthcheck/")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestRedisHealthcheckEndpoint:
    """Test cases for Redis healthcheck endpoint."""

    def test_redis_healthcheck_success(self, client):
        """Test Redis healthcheck endpoint with successful connection."""
        with patch('redis.Redis') as mock_redis_cls:
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_redis_cls.return_value = mock_client
            
            response = client.get("/healthcheck-redis/")
            
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    def test_redis_healthcheck_failure(self, client):
        """Test Redis healthcheck endpoint with connection error."""
        with patch('redis.Redis') as mock_redis_cls:
            mock_redis_cls.side_effect = Exception("Connection error")
            
            response = client.get("/healthcheck-redis/")
            
            assert response.status_code == 500
            assert "Unable to connect to Redis" in response.json()["detail"]


class TestAppInitialization:
    """Test cases for app initialization."""

    @patch('src.api.main.init_settings')
    def test_app_init_calls_init_settings(self, mock_init_settings):
        """Test that app initialization calls init_settings."""
        # Re-import to trigger initialization
        import importlib
        import src.api.main
        importlib.reload(src.api.main)
        
        mock_init_settings.assert_called_once()
