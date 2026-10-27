"""Unit tests for LLMClient module."""

from unittest.mock import MagicMock, patch

import pytest

from src.role.datastructures import LLMConfig
from src.role.llm_client import LLMClient
from src.role.prompt_repository.prompt_builder import SystemPrompt


@pytest.fixture
def llm_config():
    """Create a test LLMConfig."""
    return LLMConfig(
        model_name="test-model",
        max_tokens=100,
        temperature=0.5,
        stream=True,
        completions_url="http://test.com/v1"
    )


@pytest.fixture
def mock_lmstudio_client():
    """Mock LMStudio client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.delta = "test response"
    mock_client.stream_chat.return_value = [mock_response]
    return mock_client


class TestLLMClient:
    """Test cases for LLMClient class."""

    @patch('src.role.llm_client.LMStudio')
    def test_llm_client_init(self, mock_lmstudio_cls, llm_config):
        """Test LLMClient initialization."""
        mock_lmstudio_cls.return_value = MagicMock()
        
        client = LLMClient(config=llm_config)
        
        assert client.config == llm_config
        assert client._client is not None
        mock_lmstudio_cls.assert_called_once_with(
            model_name="test-model",
            temperature=0.5,
            base_url="http://test.com/v1"
        )

    @patch('src.role.llm_client.LMStudio')
    def test_complete_chat(self, mock_lmstudio_cls, llm_config):
        """Test complete_chat method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.delta = "test chunk"
        mock_client.stream_chat.return_value = [mock_response, mock_response]
        mock_lmstudio_cls.return_value = mock_client
        
        client = LLMClient(config=llm_config)
        chat = [["user message", "assistant message"]]
        
        result = list(client.complete_chat(chat))
        
        assert len(result) == 2
        assert all(chunk == "test chunk" for chunk in result)
        mock_client.stream_chat.assert_called_once()

    @patch('src.role.llm_client.LMStudio')
    def test_complete_chat_with_system_prompt(self, mock_lmstudio_cls, llm_config):
        """Test complete_chat with custom system prompt."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.delta = "response"
        mock_client.stream_chat.return_value = [mock_response]
        mock_lmstudio_cls.return_value = mock_client
        
        client = LLMClient(config=llm_config)
        chat = [["user", ""]]
        
        list(client.complete_chat(
            chat,
            assistant_role=SystemPrompt.COWORKER,
            additional_context="extra context"
        ))
        
        # Verify stream_chat was called with correct arguments
        mock_client.stream_chat.assert_called_once()

    @patch('src.role.llm_client.LMStudio')
    def test_convert_chat_to_chat_messages(self, mock_lmstudio_cls, llm_config):
        """Test _convert_chat_to_chat_messages method."""
        mock_lmstudio_cls.return_value = MagicMock()
        
        client = LLMClient(config=llm_config)
        chat = [
            ["user message 1", "assistant message 1"],
            ["user message 2", None]
        ]
        
        result = client._convert_chat_to_chat_messages(
            chat,
            SystemPrompt.DEFAULT,
            "additional context"
        )
        
        # Should have: system message + user1 + assistant1 + user2
        assert len(result) == 4
        assert result[0].role == "system"
        assert result[1].role == "user"
        assert result[1].content == "user message 1"
        assert result[2].role == "assistant"
        assert result[2].content == "assistant message 1"
        assert result[3].role == "user"
        assert result[3].content == "user message 2"

    @patch('src.role.llm_client.LMStudio')
    def test_convert_chat_to_chat_messages_empty_chat(self, mock_lmstudio_cls, llm_config):
        """Test _convert_chat_to_chat_messages with empty chat."""
        mock_lmstudio_cls.return_value = MagicMock()
        
        client = LLMClient(config=llm_config)
        chat = []
        
        result = client._convert_chat_to_chat_messages(chat, SystemPrompt.DEFAULT)
        
        # Should only have system message
        assert len(result) == 1
        assert result[0].role == "system"

    @patch('src.role.llm_client.LMStudio')
    def test_get_system_prompt(self, mock_lmstudio_cls, llm_config):
        """Test _get_system_prompt method."""
        mock_lmstudio_cls.return_value = MagicMock()
        
        client = LLMClient(config=llm_config)
        
        result = client._get_system_prompt(
            SystemPrompt.COWORKER,
            "additional context"
        )
        
        assert len(result) == 1
        assert result[0].role == "system"
        assert "additional context" in result[0].content

    @patch('src.role.llm_client.LMStudio')
    def test_get_system_prompt_no_additional_context(self, mock_lmstudio_cls, llm_config):
        """Test _get_system_prompt without additional context."""
        mock_lmstudio_cls.return_value = MagicMock()
        
        client = LLMClient(config=llm_config)
        
        result = client._get_system_prompt(SystemPrompt.DEFAULT)
        
        assert len(result) == 1
        assert result[0].role == "system"
        assert "additional context" not in result[0].content
