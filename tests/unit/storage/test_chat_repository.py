"""Unit tests for ChatRepository module."""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.storage.chat_repository import ChatRepository


@pytest.fixture
def mock_redis_client():
    """Mock Redis client."""
    with patch('redis.Redis') as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        yield mock_client


@pytest.fixture
def chat_repository(mock_redis_client):
    """Create a ChatRepository instance with mocked Redis."""
    return ChatRepository()


class TestChatRepositoryInit:
    """Test ChatRepository initialization."""

    def test_init_with_default_client(self, mock_redis_client):
        """Test ChatRepository initialization with default Redis client."""
        repo = ChatRepository()
        
        assert repo._client is not None
        mock_redis_client.assert_called_once()

    def test_init_with_custom_client(self):
        """Test ChatRepository initialization with custom client class."""
        custom_client_cls = MagicMock()
        custom_client = MagicMock()
        custom_client_cls.return_value = custom_client
        
        with patch('src.storage.chat_repository.redis.Redis', custom_client_cls):
            repo = ChatRepository(cache_client_cls=custom_client_cls)
        
        assert repo._client == custom_client
        custom_client_cls.assert_called_once()


class TestChatRepositoryGetCacheClient:
    """Test ChatRepository get_cache_client method."""

    @patch('os.getenv')
    def test_get_cache_client(self, mock_getenv, mock_redis_client):
        """Test get_cache_client method."""
        mock_getenv.side_effect = lambda key: {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379'
        }.get(key)
        
        repo = ChatRepository()
        client = repo.get_cache_client(redis.Redis)
        
        assert client is not None
        mock_redis_client.assert_called_once_with(host='localhost', port=6379)


class TestChatRepositoryGetChatHistory:
    """Test ChatRepository get_chat_history method."""

    def test_get_chat_history_with_data(self, mock_redis_client):
        """Test get_chat_history with existing data."""
        chat_data = [["user", "assistant"], ["user2", "assistant2"]]
        mock_redis_client.get.return_value = json.dumps(chat_data)
        
        repo = ChatRepository()
        history = repo.get_chat_history("test_session")
        
        assert history == chat_data
        mock_redis_client.get.assert_called_once_with("test_session")

    def test_get_chat_history_without_data(self, mock_redis_client):
        """Test get_chat_history with no existing data."""
        mock_redis_client.get.return_value = None
        
        repo = ChatRepository()
        history = repo.get_chat_history("test_session")
        
        assert history == []
        mock_redis_client.get.assert_called_once_with("test_session")

    def test_get_chat_history_default_session(self, mock_redis_client):
        """Test get_chat_history with default session."""
        mock_redis_client.get.return_value = None
        
        repo = ChatRepository()
        history = repo.get_chat_history()
        
        assert history == []
        mock_redis_client.get.assert_called_once_with("single_user")


class TestChatRepositoryUpdateChatHistory:
    """Test ChatRepository update_chat_history method."""

    def test_update_chat_history(self, mock_redis_client):
        """Test update_chat_history method."""
        chat_data = [["user", "assistant"]]
        
        repo = ChatRepository()
        repo.update_chat_history(chat_data, "test_session")
        
        mock_redis_client.set.assert_called_once_with(
            "test_session",
            json.dumps(chat_data)
        )

    def test_update_chat_history_default_session(self, mock_redis_client):
        """Test update_chat_history with default session."""
        chat_data = [["user", "assistant"]]
        
        repo = ChatRepository()
        repo.update_chat_history(chat_data)
        
        mock_redis_client.set.assert_called_once_with(
            "single_user",
            json.dumps(chat_data)
        )


class TestChatRepositoryResetChatHistory:
    """Test ChatRepository reset_chat_history method."""

    def test_reset_chat_history(self, mock_redis_client):
        """Test reset_chat_history method."""
        repo = ChatRepository()
        repo.reset_chat_history("test_session")
        
        mock_redis_client.delete.assert_called_once_with("test_session")

    def test_reset_chat_history_default_session(self, mock_redis_client):
        """Test reset_chat_history with default session."""
        repo = ChatRepository()
        repo.reset_chat_history()
        
        mock_redis_client.delete.assert_called_once_with("single_user")
