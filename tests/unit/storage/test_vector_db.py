"""Unit tests for vector_db module."""

from unittest.mock import MagicMock, patch

import pytest

from src.storage.vector_db import VectorStoreIndexManager
from src.role.prompt_repository.prompt_builder import SystemPrompt


@pytest.fixture
def mock_chroma():
    """Mock chromadb module."""
    with patch('chromadb.HttpClient') as mock_chroma:
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        yield mock_chroma


@pytest.fixture
def mock_vector_store():
    """Mock ChromaVectorStore."""
    return MagicMock()


@pytest.fixture
def mock_vector_store_index():
    """Mock VectorStoreIndex."""
    return MagicMock()


@pytest.fixture
def mock_storage_context():
    """Mock StorageContext."""
    return MagicMock()


@pytest.fixture
def vector_store_manager(mock_chroma, mock_vector_store, mock_vector_store_index, mock_storage_context):
    """Create a VectorStoreIndexManager instance with mocked dependencies."""
    with patch('src.storage.vector_db.ChromaVectorStore', mock_vector_store):
        with patch('src.storage.vector_db.VectorStoreIndex', mock_vector_store_index):
            with patch('src.storage.vector_db.StorageContext', mock_storage_context):
                with patch('src.storage.vector_db.DataIngestionManager') as mock_ingest_cls:
                    manager = VectorStoreIndexManager()
                    yield manager


class TestVectorStoreIndexManagerInit:
    """Test VectorStoreIndexManager initialization."""

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.VectorStoreIndex')
    @patch('src.storage.vector_db.StorageContext')
    @patch('src.storage.vector_db.DataIngestionManager')
    def test_init(self, mock_ingest_cls, mock_storage_cls, mock_index_cls, 
                 mock_vector_cls, mock_chroma):
        """Test VectorStoreIndexManager initialization."""
        mock_chroma.return_value = MagicMock()
        mock_vector_cls.return_value = MagicMock()
        mock_index_cls.return_value = MagicMock()
        mock_storage_cls.return_value = MagicMock()
        
        manager = VectorStoreIndexManager()
        
        assert manager._db_client is not None
        assert manager._collection_name == "docs_and_tickets_collection"
        assert manager._data_ingest_manager_cls == mock_ingest_cls


class TestVectorStoreIndexManagerGetIndex:
    """Test VectorStoreIndexManager get_index method."""

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.VectorStoreIndex')
    @patch('src.storage.vector_db.StorageContext')
    @patch('src.storage.vector_db.DataIngestionManager')
    def test_get_index(self, mock_ingest_cls, mock_storage_cls, mock_index_cls,
                      mock_vector_cls, mock_chroma):
        """Test get_index method."""
        mock_chroma.return_value = MagicMock()
        mock_vector_cls.return_value = MagicMock()
        mock_index = MagicMock()
        mock_index_cls.from_vector_store.return_value = mock_index
        mock_storage_cls.from_defaults.return_value = MagicMock()
        
        manager = VectorStoreIndexManager()
        
        result = manager.get_index()
        
        assert result == mock_index


class TestVectorStoreIndexManagerGetChatEngine:
    """Test VectorStoreIndexManager get_chat_engine method."""

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.VectorStoreIndex')
    @patch('src.storage.vector_db.StorageContext')
    @patch('src.storage.vector_db.DataIngestionManager')
    def test_get_chat_engine(self, mock_ingest_cls, mock_storage_cls, mock_index_cls,
                            mock_vector_cls, mock_chroma):
        """Test get_chat_engine method."""
        mock_chroma.return_value = MagicMock()
        mock_vector_cls.return_value = MagicMock()
        mock_index = MagicMock()
        mock_chat_engine = MagicMock()
        mock_index.as_chat_engine.return_value = mock_chat_engine
        mock_index_cls.from_vector_store.return_value = mock_index
        mock_storage_cls.from_defaults.return_value = MagicMock()
        
        manager = VectorStoreIndexManager()
        
        result = manager.get_chat_engine()
        
        assert result == mock_chat_engine
        mock_index.as_chat_engine.assert_called_once()


class TestVectorStoreIndexManagerReindex:
    """Test VectorStoreIndexManager reindex_documents method."""

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.VectorStoreIndex')
    @patch('src.storage.vector_db.StorageContext')
    @patch('src.storage.vector_db.DataIngestionManager')
    def test_reindex_documents(self, mock_ingest_cls, mock_storage_cls, mock_index_cls,
                               mock_vector_cls, mock_chroma):
        """Test reindex_documents method."""
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        mock_vector_cls.return_value = MagicMock()
        mock_index_cls.from_vector_store.return_value = MagicMock()
        mock_storage_cls.from_defaults.return_value = MagicMock()
        
        manager = VectorStoreIndexManager()
        
        manager.reindex_documents()
        
        mock_client.delete_collection.assert_called_once_with("docs_and_tickets_collection")
        mock_client.get_or_create_collection.assert_called_once_with("docs_and_tickets_collection")


class TestVectorStoreIndexManagerPrivateMethods:
    """Test VectorStoreIndexManager private methods."""

    @patch('chromadb.HttpClient')
    def test_get_db_client(self, mock_chroma):
        """Test _get_db_client method."""
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        
        with patch('os.getenv', side_effect=lambda k: {
            'CHROMADB_HOST': 'localhost',
            'CHROMADB_PORT': '8000'
        }.get(k)):
            manager = VectorStoreIndexManager()
            
            result = manager._get_db_client()
            
            assert result == mock_client
            mock_chroma.assert_called_once_with(host='localhost', port='8000')

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    def test_get_or_create_collection(self, mock_vector_cls, mock_chroma):
        """Test _get_or_create_collection method."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.return_value = mock_client
        mock_vector_cls.return_value = MagicMock()
        
        manager = VectorStoreIndexManager()
        
        result = manager._get_or_create_collection()
        
        assert result == mock_collection
        mock_client.get_or_create_collection.assert_called_once_with("docs_and_tickets_collection")

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    def test_get_vector_store(self, mock_vector_cls, mock_chroma):
        """Test _get_vector_store method."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.return_value = mock_client
        
        mock_vector = MagicMock()
        mock_vector_cls.from_collection.return_value = mock_vector
        
        manager = VectorStoreIndexManager()
        
        result = manager._get_vector_store()
        
        assert result == mock_vector
        mock_vector_cls.from_collection.assert_called_once_with(collection=mock_collection)

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.StorageContext')
    def test_get_storage_context(self, mock_storage_cls, mock_vector_cls, mock_chroma):
        """Test _get_storage_context method."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.return_value = mock_client
        
        mock_vector = MagicMock()
        mock_vector_cls.from_collection.return_value = mock_vector
        
        mock_storage = MagicMock()
        mock_storage_cls.from_defaults.return_value = mock_storage
        
        manager = VectorStoreIndexManager()
        
        result = manager._get_storage_context()
        
        assert result == mock_storage
        mock_storage_cls.from_defaults.assert_called_once_with(vector_store=mock_vector)

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.VectorStoreIndex')
    @patch('src.storage.vector_db.StorageContext')
    def test_get_index_private(self, mock_storage_cls, mock_index_cls, mock_vector_cls, mock_chroma):
        """Test _get_index private method."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.return_value = mock_client
        
        mock_vector = MagicMock()
        mock_vector_cls.from_collection.return_value = mock_vector
        
        mock_storage = MagicMock()
        mock_storage_cls.from_defaults.return_value = mock_storage
        
        mock_index = MagicMock()
        mock_index_cls.from_vector_store.return_value = mock_index
        
        manager = VectorStoreIndexManager()
        
        result = manager._get_index()
        
        assert result == mock_index

    @patch('chromadb.HttpClient')
    @patch('src.storage.vector_db.ChromaVectorStore')
    @patch('src.storage.vector_db.DataIngestionManager')
    def test_load_documents(self, mock_ingest_cls, mock_vector_cls, mock_chroma):
        """Test _load_documents method."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        mock_chroma.return_value = mock_client
        
        mock_vector = MagicMock()
        mock_vector_cls.from_collection.return_value = mock_vector
        
        mock_ingest_manager = MagicMock()
        mock_ingest_cls.return_value = mock_ingest_manager
        
        manager = VectorStoreIndexManager()
        
        manager._load_documents()
        
        assert mock_ingest_manager.run_ingestion_pipeline.call_count == 2
        mock_ingest_manager.run_ingestion_pipeline.assert_any_call_with(document_type="tickets")
        mock_ingest_manager.run_ingestion_pipeline.assert_any_call_with(document_type="documentation")

    @patch('chromadb.HttpClient')
    def test_remove_documents(self, mock_chroma):
        """Test _remove_documents method."""
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        
        manager = VectorStoreIndexManager()
        
        manager._remove_documents()
        
        mock_client.delete_collection.assert_called_once_with("docs_and_tickets_collection")

    @patch('chromadb.HttpClient')
    def test_remove_documents_collection_not_found(self, mock_chroma):
        """Test _remove_documents when collection doesn't exist."""
        mock_client = MagicMock()
        mock_client.delete_collection.side_effect = Exception(
            "Collection docs_and_tickets_collection does not exist."
        )
        mock_chroma.return_value = mock_client
        
        manager = VectorStoreIndexManager()
        
        # Should not raise exception
        manager._remove_documents()
        
        mock_client.delete_collection.assert_called_once_with("docs_and_tickets_collection")
