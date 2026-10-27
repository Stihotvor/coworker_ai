"""Unit tests for custom_transformations module."""

from unittest.mock import MagicMock

import pytest

from src.storage.custom_transformations import TextCleaner, DocumentTypeToMetadata


@pytest.fixture
def mock_node():
    """Create a mock BaseNode."""
    node = MagicMock()
    node.text = "Test text with special chars! @#$"
    node.metadata = {}
    return node


class TestTextCleaner:
    """Test cases for TextCleaner class."""

    def test_text_cleaner_call(self, mock_node):
        """Test TextCleaner __call__ method."""
        cleaner = TextCleaner()
        nodes = [mock_node]
        
        result = cleaner(nodes)
        
        assert len(result) == 1
        assert result[0] == mock_node
        # Text should be cleaned (remove non-alphanumeric except space)
        assert mock_node.text == "Test text with special chars "

    def test_text_cleaner_multiple_nodes(self, mock_node):
        """Test TextCleaner with multiple nodes."""
        cleaner = TextCleaner()
        nodes = [mock_node, mock_node, mock_node]
        
        result = cleaner(nodes)
        
        assert len(result) == 3
        for node in result:
            assert node.text == "Test text with special chars "

    def test_text_cleaner_empty_list(self):
        """Test TextCleaner with empty list."""
        cleaner = TextCleaner()
        nodes = []
        
        result = cleaner(nodes)
        
        assert result == []


class TestDocumentTypeToMetadata:
    """Test cases for DocumentTypeToMetadata class."""

    def test_document_type_to_metadata_call(self, mock_node):
        """Test DocumentTypeToMetadata __call__ method."""
        transformer = DocumentTypeToMetadata(document_type="tickets")
        nodes = [mock_node]
        
        result = transformer(nodes, document_type="tickets")
        
        assert len(result) == 1
        assert result[0] == mock_node
        assert mock_node.metadata["document_type"] == "tickets"

    def test_document_type_to_metadata_different_type(self, mock_node):
        """Test DocumentTypeToMetadata with different document type."""
        transformer = DocumentTypeToMetadata(document_type="documentation")
        nodes = [mock_node]
        
        result = transformer(nodes, document_type="documentation")
        
        assert len(result) == 1
        assert mock_node.metadata["document_type"] == "documentation"

    def test_document_type_to_metadata_multiple_nodes(self, mock_node):
        """Test DocumentTypeToMetadata with multiple nodes."""
        transformer = DocumentTypeToMetadata(document_type="tickets")
        nodes = [mock_node, mock_node]
        
        result = transformer(nodes, document_type="tickets")
        
        assert len(result) == 2
        for node in result:
            assert node.metadata["document_type"] == "tickets"

    def test_document_type_to_metadata_empty_list(self):
        """Test DocumentTypeToMetadata with empty list."""
        transformer = DocumentTypeToMetadata(document_type="tickets")
        nodes = []
        
        result = transformer(nodes, document_type="tickets")
        
        assert result == []

    def test_document_type_to_metadata_preserves_existing_metadata(self, mock_node):
        """Test DocumentTypeToMetadata preserves existing metadata."""
        mock_node.metadata = {"existing_key": "existing_value"}
        
        transformer = DocumentTypeToMetadata(document_type="tickets")
        nodes = [mock_node]
        
        result = transformer(nodes, document_type="tickets")
        
        assert len(result) == 1
        assert result[0].metadata["existing_key"] == "existing_value"
        assert result[0].metadata["document_type"] == "tickets"
