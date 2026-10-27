"""Pytest configuration and fixtures for coworker_ai tests."""

import os
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# Mock External Dependencies
# =============================================================================


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    with patch('redis.Redis') as mock_redis_cls:
        mock_client = MagicMock()
        mock_redis_cls.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_chroma_client():
    """Mock ChromaDB client for testing."""
    with patch('chromadb.HttpClient') as mock_chroma:
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_lm_studio():
    """Mock LMStudio client for testing."""
    with patch('llama_index.llms.lmstudio.LMStudio') as mock_lm:
        mock_client = MagicMock()
        mock_lm.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for LMStudio embeddings."""
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        yield mock_client


# =============================================================================
# Test Data Factories
# =============================================================================


@pytest.fixture
def llm_config_data():
    """Factory for LLMConfig test data."""
    return {
        'model_name': 'test-model',
        'max_tokens': 100,
        'temperature': 0.5,
        'stream': True,
        'completions_url': 'http://test.com/completions'
    }


@pytest.fixture
def task_data():
    """Factory for Task test data."""
    from src.ui.datastructures import Task, TaskStatus
    
    return {
        'id': 'TASK-0001',
        'title': 'Test Task',
        'status': TaskStatus.TO_DO,
        'responsible_person': 'test-user',
        'context': 'Test context'
    }


@pytest.fixture
def document_data():
    """Factory for Document test data."""
    return {
        'id': 'DOC-0001',
        'title': 'Test Document',
        'context': 'Test document content'
    }


@pytest.fixture
def chat_history_data():
    """Factory for chat history test data."""
    return [
        ['Hello', 'Hi there!'],
        ['How are you?', 'I am good, thanks!']
    ]


# =============================================================================
# Environment Setup
# =============================================================================


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set common environment variables for testing
    os.environ['REDIS_HOST'] = 'localhost'
    os.environ['REDIS_PORT'] = '6379'
    os.environ['CHROMADB_HOST'] = 'localhost'
    os.environ['CHROMADB_PORT'] = '8000'
    
    yield
    
    # Clean up
    for key in ['REDIS_HOST', 'REDIS_PORT', 'CHROMADB_HOST', 'CHROMADB_PORT']:
        os.environ.pop(key, None)


# =============================================================================
# Pytest Configuration
# =============================================================================

def pytest_configure(config):
    """Pytest configuration."""
    # Add custom markers
    config.addinivalue_line(
        'markers',
        'unit: mark a test as a unit test'
    )
    config.addinivalue_line(
        'markers',
        'integration: mark a test as an integration test'
    )
    config.addinivalue_line(
        'markers',
        'slow: mark a test as slow (takes > 1 second)'
    )


# =============================================================================
# Coverage Configuration
# =============================================================================

# This is configured in pyproject.toml, but can be overridden here if needed
# pytest_cov = pytest.importorskip('pytest_cov')
