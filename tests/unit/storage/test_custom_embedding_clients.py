"""Unit tests for custom_embedding_clients module."""

from unittest.mock import MagicMock, patch

import pytest

from src.storage.custom_embedding_clients.lm_studio_client import LMStudioEmbedding


@pytest.fixture
def mock_callback_manager():
    """Mock CallbackManager."""
    return MagicMock()


@pytest.fixture
def embedding_client(mock_callback_manager):
    """Create an LMStudioEmbedding instance."""
    return LMStudioEmbedding(
        model_name="test-model",
        base_url="http://test.com/v1",
        embed_batch_size=32,
        callback_manager=mock_callback_manager
    )


class TestLMStudioEmbeddingInit:
    """Test LMStudioEmbedding initialization."""

    def test_init_with_defaults(self):
        """Test LMStudioEmbedding initialization with defaults."""
        client = LMStudioEmbedding(
            model_name="test-model",
            base_url="http://test.com/v1"
        )
        
        assert client.model_name == "test-model"
        assert client.base_url == "http://test.com/v1"
        assert client.embed_batch_size == 32  # DEFAULT_EMBED_BATCH_SIZE

    def test_init_with_custom_values(self):
        """Test LMStudioEmbedding initialization with custom values."""
        client = LMStudioEmbedding(
            model_name="custom-model",
            base_url="http://custom.com/v1",
            embed_batch_size=64
        )
        
        assert client.model_name == "custom-model"
        assert client.base_url == "http://custom.com/v1"
        assert client.embed_batch_size == 64


class TestLMStudioEmbeddingClassName:
    """Test LMStudioEmbedding class_name method."""

    def test_class_name(self):
        """Test class_name class method."""
        assert LMStudioEmbedding.class_name() == "LMStudioEmbedding"


class TestLMStudioEmbeddingEmbeddings:
    """Test LMStudioEmbedding embedding methods."""

    @patch('openai.OpenAI')
    def test_get_query_embedding(self, mock_openai, embedding_client):
        """Test _get_query_embedding method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = embedding_client._get_query_embedding("test query")
        
        assert result == [0.1, 0.2, 0.3]
        mock_client.embeddings.create.assert_called_once()

    @patch('openai.OpenAI')
    async def test_aget_query_embedding(self, mock_openai, embedding_client):
        """Test _aget_query_embedding method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.4, 0.5, 0.6]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = await embedding_client._aget_query_embedding("test query")
        
        assert result == [0.4, 0.5, 0.6]

    @patch('openai.OpenAI')
    def test_get_text_embedding(self, mock_openai, embedding_client):
        """Test _get_text_embedding method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.7, 0.8, 0.9]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = embedding_client._get_text_embedding("test text")
        
        assert result == [0.7, 0.8, 0.9]

    @patch('openai.OpenAI')
    def test_get_text_embeddings(self, mock_openai, embedding_client):
        """Test _get_text_embeddings method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [1.0, 2.0, 3.0]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        texts = ["text1", "text2", "text3"]
        result = embedding_client._get_text_embeddings(texts)
        
        assert len(result) == 3
        assert all(embedding == [1.0, 2.0, 3.0] for embedding in result)

    @patch('openai.OpenAI')
    async def test_aget_text_embeddings(self, mock_openai, embedding_client):
        """Test _aget_text_embeddings method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [4.0, 5.0, 6.0]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        texts = ["text1", "text2"]
        result = await embedding_client._aget_text_embeddings(texts)
        
        assert len(result) == 2
        assert all(embedding == [4.0, 5.0, 6.0] for embedding in result)


class TestLMStudioEmbeddingGeneral:
    """Test LMStudioEmbedding general embedding method."""

    @patch('openai.OpenAI')
    def test_get_general_text_embedding(self, mock_openai, embedding_client):
        """Test get_general_text_embedding method."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = embedding_client.get_general_text_embedding("test prompt")
        
        assert result == [0.1, 0.2, 0.3]
        mock_client.embeddings.create.assert_called_once()

    @patch('openai.OpenAI')
    def test_get_general_text_embedding_with_dimensions(self, mock_openai, embedding_client):
        """Test get_general_text_embedding with dimensions."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = embedding_client.get_general_text_embedding(
            "test prompt",
            dimensions=128
        )
        
        assert result == [0.1, 0.2, 0.3]
        # Verify dimensions parameter was passed
        call_kwargs = mock_client.embeddings.create.call_args[1]
        assert call_kwargs['dimensions'] == 128

    @patch('openai.OpenAI')
    def test_get_general_text_embedding_newlines(self, mock_openai, embedding_client):
        """Test get_general_text_embedding handles newlines."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        result = embedding_client.get_general_text_embedding("test\nprompt")
        
        assert result == [0.1, 0.2, 0.3]
        # Verify newline was replaced with space
        call_args = mock_client.embeddings.create.call_args[1]
        assert call_args['input'][0] == "test prompt"
