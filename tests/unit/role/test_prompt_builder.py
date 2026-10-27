"""Unit tests for prompt_builder module."""

import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from src.role.prompt_repository.prompt_builder import SystemPrompt, collect_prompt


@pytest.fixture
def temp_prompt_file():
    """Create a temporary prompt file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("Test prompt content")
        f.flush()
        yield f.name
    os.unlink(f.name)


class TestCollectPrompt:
    """Test cases for collect_prompt function."""

    def test_collect_prompt_success(self, temp_prompt_file):
        """Test collect_prompt with valid file."""
        # Temporarily override the file path
        with patch('src.role.prompt_repository.prompt_builder.open') as mock_open:
            mock_file = MagicMock()
            mock_file.read.return_value = "Test prompt content"
            mock_open.return_value.__enter__.return_value = mock_file
            
            result = collect_prompt("test", "system")
            
            assert result == "Test prompt content"
            mock_open.assert_called_once()

    def test_collect_prompt_file_not_found(self):
        """Test collect_prompt with non-existent file."""
        with patch('src.role.prompt_repository.prompt_builder.open') as mock_open:
            mock_open.side_effect = FileNotFoundError("File not found")
            
            with pytest.raises(FileNotFoundError):
                collect_prompt("nonexistent", "system")


class TestSystemPrompt:
    """Test cases for SystemPrompt enum."""

    def test_system_prompt_default(self):
        """Test SystemPrompt.DEFAULT."""
        # Read actual content from file
        with open("src/role/prompt_repository/system/default.md", "r") as f:
            expected_content = f.read()
        
        assert SystemPrompt.DEFAULT.value == expected_content

    def test_system_prompt_coworker(self):
        """Test SystemPrompt.COWORKER."""
        # Read actual content from file
        with open("src/role/prompt_repository/system/coworker.md", "r") as f:
            expected_content = f.read()
        
        assert SystemPrompt.COWORKER.value == expected_content

    def test_system_prompt_enum_values(self):
        """Test SystemPrompt enum has expected values."""
        assert hasattr(SystemPrompt, 'DEFAULT')
        assert hasattr(SystemPrompt, 'COWORKER')
