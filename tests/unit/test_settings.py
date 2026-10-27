"""Unit tests for settings module."""

from unittest.mock import MagicMock, patch

import pytest

from src.settings import (
    init_llm_config,
    init_embedding_config,
    init_text_splitter,
    init_settings
)


@pytest.fixture
def mock_settings():
    """Mock Settings object."""
    return MagicMock()


class TestInitLLMConfig:
    """Test cases for init_llm_config function."""

    @patch('src.settings.LMStudio')
    def test_init_llm_config(self, mock_lmstudio_cls, mock_settings):
        """Test init_llm_config sets up LLM correctly."""
        mock_lmstudio = MagicMock()
        mock_lmstudio_cls.return_value = mock_lmstudio
        
        init_llm_config(mock_settings)
        
        assert mock_settings.llm == mock_lmstudio
        mock_lmstudio_cls.assert_called_once_with(
            model_name="TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q2_K.gguf",
            base_url="http://host.docker.internal:1234/v1",
            temperature=0.5,
            timeout=600,
            request_timeout=600
        )


class TestInitEmbeddingConfig:
    """Test cases for init_embedding_config function."""

    @patch('src.settings.LMStudioEmbedding')
    def test_init_embedding_config(self, mock_embedding_cls, mock_settings):
        """Test init_embedding_config sets up embedding model correctly."""
        mock_embedding = MagicMock()
        mock_embedding_cls.return_value = mock_embedding
        
        init_embedding_config(mock_settings)
        
        assert mock_settings.embed_model == mock_embedding
        mock_embedding_cls.assert_called_once_with(
            base_url="http://host.docker.internal:1234/v1",
            model_name="all-MiniLM-L6-v2-ggml-model-f16"
        )


class TestInitTextSplitter:
    """Test cases for init_text_splitter function."""

    @patch('src.settings.SemanticSplitterNodeParser')
    def test_init_text_splitter(self, mock_splitter_cls, mock_settings):
        """Test init_text_splitter sets up text splitter correctly."""
        mock_splitter = MagicMock()
        mock_splitter_cls.return_value = mock_splitter
        mock_settings.embed_model = MagicMock()
        
        init_text_splitter(mock_settings)
        
        assert mock_settings.text_splitter == mock_splitter
        mock_splitter_cls.assert_called_once_with(
            buffer_size=1,
            breakpoint_percentile_threshold=95,
            embed_model=mock_settings.embed_model
        )


class TestInitSettings:
    """Test cases for init_settings function."""

    @patch('src.settings.init_llm_config')
    @patch('src.settings.init_embedding_config')
    @patch('src.settings.init_text_splitter')
    def test_init_settings(self, mock_init_text, mock_init_embed, mock_init_llm, mock_settings):
        """Test init_settings calls all initialization functions."""
        init_settings(mock_settings)
        
        mock_init_llm.assert_called_once_with(mock_settings)
        mock_init_embed.assert_called_once_with(mock_settings)
        mock_init_text.assert_called_once_with(mock_settings)
