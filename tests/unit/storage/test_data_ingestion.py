"""Unit tests for data_ingestion module."""

from unittest.mock import MagicMock, patch

import pytest

from src.storage.data_ingestion import DataIngestionManager, DOCUMENT_PATHS


@pytest.fixture
def mock_vector_store():
    """Mock ChromaVectorStore."""
    return MagicMock()


@pytest.fixture
def mock_settings():
    """Mock Settings."""
    return MagicMock()


@pytest.fixture
def data_ingestion_manager(mock_vector_store, mock_settings):
    """Create a DataIngestionManager instance with mocked dependencies."""
    with patch('src.storage.data_ingestion.Settings', mock_settings):
        with patch('src.storage.data_ingestion.IngestionPipeline') as mock_pipeline_cls:
            with patch('src.storage.data_ingestion.IngestionCache') as mock_cache_cls:
                with patch('src.storage.data_ingestion.RedisKVStore') as mock_kvstore_cls:
                    mock_pipeline = MagicMock()
                    mock_pipeline_cls.return_value = mock_pipeline
                    
                    manager = DataIngestionManager(
                        vector_store=mock_vector_store,
                        cache_collection="test_collection"
                    )
                    yield manager


class TestDataIngestionManagerConstants:
    """Test DataIngestionManager constants."""

    def test_document_paths(self):
        """Test DOCUMENT_PATHS constant."""
        assert "tickets" in DOCUMENT_PATHS
        assert "documentation" in DOCUMENT_PATHS
        assert DOCUMENT_PATHS["tickets"] == "data/tickets"
        assert DOCUMENT_PATHS["documentation"] == "data/documentation"


class TestDataIngestionManagerInit:
    """Test DataIngestionManager initialization."""

    @patch('src.storage.data_ingestion.Settings')
    @patch('src.storage.data_ingestion.IngestionPipeline')
    @patch('src.storage.data_ingestion.IngestionCache')
    @patch('src.storage.data_ingestion.RedisKVStore')
    def test_init(self, mock_kvstore_cls, mock_cache_cls, mock_pipeline_cls, mock_settings):
        """Test DataIngestionManager initialization."""
        mock_vector_store = MagicMock()
        
        manager = DataIngestionManager(
            vector_store=mock_vector_store,
            cache_collection="test_collection"
        )
        
        assert manager._vector_store == mock_vector_store
        assert manager._ingestion_pipeline_cls == mock_pipeline_cls
        assert manager._settings == mock_settings
        assert manager._ingest_cache is not None


class TestDataIngestionManagerRunPipeline:
    """Test DataIngestionManager run_ingestion_pipeline method."""

    @patch('src.storage.data_ingestion.SimpleDirectoryReader')
    @patch('src.storage.data_ingestion.Settings')
    @patch('src.storage.data_ingestion.IngestionPipeline')
    @patch('src.storage.data_ingestion.IngestionCache')
    @patch('src.storage.data_ingestion.RedisKVStore')
    def test_run_ingestion_pipeline_tickets(self, mock_kvstore_cls, mock_cache_cls, 
                                          mock_pipeline_cls, mock_settings, 
                                          mock_directory_reader):
        """Test run_ingestion_pipeline for tickets."""
        mock_vector_store = MagicMock()
        mock_pipeline = MagicMock()
        mock_pipeline_cls.return_value = mock_pipeline
        
        mock_documents = [MagicMock()]
        mock_directory_reader.return_value.load_data.return_value = mock_documents
        
        with patch('os.getenv', side_effect=lambda k: {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379'
        }.get(k)):
            manager = DataIngestionManager(
                vector_store=mock_vector_store,
                cache_collection="test_collection"
            )
            
            manager.run_ingestion_pipeline(document_type="tickets")
            
            mock_directory_reader.assert_called_once_with("data/tickets")
            mock_pipeline_cls.assert_called_once()
            mock_pipeline.run.assert_called_once()

    @patch('src.storage.data_ingestion.SimpleDirectoryReader')
    @patch('src.storage.data_ingestion.Settings')
    @patch('src.storage.data_ingestion.IngestionPipeline')
    @patch('src.storage.data_ingestion.IngestionCache')
    @patch('src.storage.data_ingestion.RedisKVStore')
    def test_run_ingestion_pipeline_documentation(self, mock_kvstore_cls, mock_cache_cls,
                                                 mock_pipeline_cls, mock_settings,
                                                 mock_directory_reader):
        """Test run_ingestion_pipeline for documentation."""
        mock_vector_store = MagicMock()
        mock_pipeline = MagicMock()
        mock_pipeline_cls.return_value = mock_pipeline
        
        mock_documents = [MagicMock()]
        mock_directory_reader.return_value.load_data.return_value = mock_documents
        
        with patch('os.getenv', side_effect=lambda k: {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379'
        }.get(k)):
            manager = DataIngestionManager(
                vector_store=mock_vector_store,
                cache_collection="test_collection"
            )
            
            manager.run_ingestion_pipeline(document_type="documentation")
            
            mock_directory_reader.assert_called_once_with("data/documentation")


class TestDataIngestionManagerPrivateMethods:
    """Test DataIngestionManager private methods."""

    @patch('src.storage.data_ingestion.Settings')
    @patch('src.storage.data_ingestion.IngestionPipeline')
    @patch('src.storage.data_ingestion.IngestionCache')
    @patch('src.storage.data_ingestion.RedisKVStore')
    def test_run_ingestion_pipeline(self, mock_kvstore_cls, mock_cache_cls,
                                    mock_pipeline_cls, mock_settings):
        """Test _run_ingestion_pipeline method."""
        mock_vector_store = MagicMock()
        mock_pipeline = MagicMock()
        mock_pipeline_cls.return_value = mock_pipeline
        
        mock_documents = [MagicMock()]
        
        with patch('os.getenv', side_effect=lambda k: {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379'
        }.get(k)):
            manager = DataIngestionManager(
                vector_store=mock_vector_store,
                cache_collection="test_collection"
            )
            
            manager._run_ingestion_pipeline(mock_documents, document_type="tickets")
            
            mock_pipeline_cls.assert_called_once()
            mock_pipeline.run.assert_called_once()

    @patch('src.storage.data_ingestion.Settings')
    @patch('src.storage.data_ingestion.IngestionPipeline')
    @patch('src.storage.data_ingestion.IngestionCache')
    @patch('src.storage.data_ingestion.RedisKVStore')
    def test_setup_cache(self, mock_kvstore_cls, mock_cache_cls,
                         mock_pipeline_cls, mock_settings):
        """Test _setup_cache method."""
        mock_vector_store = MagicMock()
        mock_cache_instance = MagicMock()
        mock_cache_cls.return_value = mock_cache_instance
        
        mock_kvstore_instance = MagicMock()
        mock_kvstore_cls.from_host_and_port.return_value = mock_kvstore_instance
        
        with patch('os.getenv', side_effect=lambda k: {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379'
        }.get(k)):
            manager = DataIngestionManager(
                vector_store=mock_vector_store,
                cache_collection="test_collection"
            )
            
            cache = manager._setup_cache(
                mock_cache_cls,
                mock_kvstore_cls,
                "test_collection"
            )
            
            assert cache == mock_cache_instance
            mock_kvstore_cls.from_host_and_port.assert_called_once_with(
                host='localhost',
                port=6379
            )

    @patch('src.storage.data_ingestion.SimpleDirectoryReader')
    def test_load_documents(self, mock_directory_reader):
        """Test _load_documents method."""
        mock_documents = [MagicMock(), MagicMock()]
        mock_directory_reader.return_value.load_data.return_value = mock_documents
        
        with patch('src.storage.data_ingestion.Settings') as mock_settings:
            with patch('src.storage.data_ingestion.IngestionPipeline') as mock_pipeline_cls:
                with patch('src.storage.data_ingestion.IngestionCache') as mock_cache_cls:
                    with patch('src.storage.data_ingestion.RedisKVStore') as mock_kvstore_cls:
                        manager = DataIngestionManager(
                            vector_store=MagicMock(),
                            cache_collection="test_collection"
                        )
                        
                        result = manager._load_documents("data/tickets")
                        
                        assert result == mock_documents
                        mock_directory_reader.assert_called_once_with("data/tickets")
