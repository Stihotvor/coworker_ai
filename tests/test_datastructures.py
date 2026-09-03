"""Tests for datastructures module."""

import pytest
from src.role.datastructures import LLMConfig


class TestLLMConfig:
    """Test cases for LLMConfig dataclass."""

    def test_llm_config_default_values(self):
        """Test LLMConfig with default values."""
        config = LLMConfig(
            model_name="test-model",
            max_tokens=100,
            temperature=0.5,
            stream=True,
            completions_url="http://test.com/completions"
        )
        assert config.model_name == "test-model"
        assert config.max_tokens == 100
        assert config.temperature == 0.5
        assert config.stream is True
        assert config.completions_url == "http://test.com/completions"

    def test_llm_config_different_values(self):
        """Test LLMConfig with different values."""
        config = LLMConfig(
            model_name="another-model",
            max_tokens=200,
            temperature=0.7,
            stream=False,
            completions_url="http://another.com/completions"
        )
        assert config.model_name == "another-model"
        assert config.max_tokens == 200
        assert config.temperature == 0.7
        assert config.stream is False
        assert config.completions_url == "http://another.com/completions"

    def test_llm_config_equality(self):
        """Test equality comparison for LLMConfig."""
        config1 = LLMConfig(
            model_name="model",
            max_tokens=100,
            temperature=0.5,
            stream=True,
            completions_url="http://test.com"
        )
        config2 = LLMConfig(
            model_name="model",
            max_tokens=100,
            temperature=0.5,
            stream=True,
            completions_url="http://test.com"
        )
        assert config1 == config2

    def test_llm_config_inequality(self):
        """Test inequality comparison for LLMConfig."""
        config1 = LLMConfig(
            model_name="model1",
            max_tokens=100,
            temperature=0.5,
            stream=True,
            completions_url="http://test.com"
        )
        config2 = LLMConfig(
            model_name="model2",
            max_tokens=100,
            temperature=0.5,
            stream=True,
            completions_url="http://test.com"
        )
        assert config1 != config2
