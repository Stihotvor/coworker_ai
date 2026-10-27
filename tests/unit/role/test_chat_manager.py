"""Unit tests for ChatManager module."""

from unittest.mock import MagicMock, patch, call

import pytest

from src.role.chat_manager import ChatManager
from src.ui.datastructures import RelatedTasks, RelatedDocuments, Task, TaskStatus, Document


@pytest.fixture
def mock_chat_repository():
    """Mock ChatRepository."""
    with patch('src.role.chat_manager.ChatRepository') as mock_cls:
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = []
        mock_repo.update_chat_history.return_value = None
        mock_cls.return_value = mock_repo
        yield mock_repo


@pytest.fixture
def mock_vector_store():
    """Mock VectorStoreIndexManager."""
    with patch('src.role.chat_manager.VectorStoreIndexManager') as mock_cls:
        mock_store = MagicMock()
        mock_chat_engine = MagicMock()
        mock_response = MagicMock()
        mock_response.source_nodes = []
        mock_response.response_gen = iter(["chunk1", "chunk2"])
        mock_chat_engine.stream_chat.return_value = mock_response
        mock_store.get_chat_engine.return_value = mock_chat_engine
        mock_cls.return_value = mock_store
        yield mock_store


@pytest.fixture
def chat_manager(mock_chat_repository, mock_vector_store):
    """Create a ChatManager instance with mocked dependencies."""
    return ChatManager(
        ui_info_log=MagicMock(),
        ui_error_log=MagicMock()
    )


class TestChatManagerInit:
    """Test ChatManager initialization."""

    def test_init_with_defaults(self, mock_chat_repository, mock_vector_store):
        """Test ChatManager initialization with default classes."""
        ui_info_log = MagicMock()
        ui_error_log = MagicMock()
        
        manager = ChatManager(
            ui_info_log=ui_info_log,
            ui_error_log=ui_error_log
        )
        
        assert manager._ui_info_log == ui_info_log
        assert manager._ui_error_log == ui_error_log
        assert manager.chat_repository is not None
        assert manager._store is not None
        assert isinstance(manager._related_tasks, RelatedTasks)
        assert isinstance(manager._related_documents, RelatedDocuments)

    def test_init_with_custom_classes(self, mock_chat_repository, mock_vector_store):
        """Test ChatManager initialization with custom classes."""
        custom_repo_cls = MagicMock()
        custom_store_cls = MagicMock()
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock(),
            chat_repository_cls=custom_repo_cls,
            vector_store_index_cls=custom_store_cls
        )
        
        custom_repo_cls.assert_called_once()
        custom_store_cls.assert_called_once()


class TestChatManagerReset:
    """Test ChatManager reset methods."""

    def test_reset_chat_history(self, chat_manager, mock_chat_repository):
        """Test reset_chat_history method."""
        chat_manager.reset_chat_history()
        
        mock_chat_repository.reset_chat_history.assert_called_once_with()
        chat_manager._ui_info_log.assert_called_with("Chat history is reset")

    def test_reset_related_tasks(self, chat_manager):
        """Test reset_related_tasks method."""
        # Set some tasks first
        task = Task(id="TASK-0001", title="Test", status=TaskStatus.TO_DO)
        chat_manager._related_tasks.task_1 = task
        
        chat_manager.reset_related_tasks()
        
        assert isinstance(chat_manager._related_tasks, RelatedTasks)
        assert chat_manager._related_tasks.task_1.id == "TASK-0000"

    def test_reset_related_documents(self, chat_manager):
        """Test reset_related_documents method."""
        # Set some documents first
        doc = Document(id="DOC-0001", title="Test", context="test")
        chat_manager._related_documents.document_1 = doc
        
        chat_manager.reset_related_documents()
        
        assert isinstance(chat_manager._related_documents, RelatedDocuments)
        assert chat_manager._related_documents.document_1.id == "DOC-0000"


class TestChatManagerReindex:
    """Test ChatManager reindex_documents method."""

    def test_reindex_documents(self, chat_manager, mock_vector_store):
        """Test reindex_documents method."""
        chat_manager.reindex_documents()
        
        mock_vector_store.reindex_documents.assert_called_once()
        chat_manager._ui_info_log.assert_called_with("Documents are re-indexed")


class TestChatManagerPredict:
    """Test ChatManager predict method."""

    @patch('src.role.chat_manager.ChatRepository')
    @patch('src.role.chat_manager.VectorStoreIndexManager')
    def test_predict_empty_query(self, mock_store_cls, mock_repo_cls):
        """Test predict with empty query."""
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = []
        mock_repo_cls.return_value = mock_repo
        
        mock_store = MagicMock()
        mock_store_cls.return_value = mock_store
        
        ui_error_log = MagicMock()
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=ui_error_log
        )
        
        result = list(manager.predict(""))
        
        assert len(result) == 1
        ui_error_log.assert_called_with("Please, provide a valid query.")

    @patch('src.role.chat_manager.ChatRepository')
    @patch('src.role.chat_manager.VectorStoreIndexManager')
    def test_predict_valid_query(self, mock_store_cls, mock_repo_cls):
        """Test predict with valid query."""
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = []
        mock_repo.update_chat_history.return_value = None
        mock_repo_cls.return_value = mock_repo
        
        mock_store = MagicMock()
        mock_chat_engine = MagicMock()
        mock_response = MagicMock()
        mock_response.source_nodes = []
        mock_response.response_gen = iter(["chunk1", "chunk2"])
        mock_chat_engine.stream_chat.return_value = mock_response
        mock_store.get_chat_engine.return_value = mock_chat_engine
        mock_store_cls.return_value = mock_store
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        result = list(manager.predict("test query"))
        
        assert len(result) == 2
        mock_repo.get_chat_history.assert_called()
        mock_chat_engine.stream_chat.assert_called_once()


class TestChatManagerRelatedItems:
    """Test ChatManager related items methods."""

    def test_get_related_tasks_titles(self, chat_manager):
        """Test get_related_tasks_titles method."""
        titles = chat_manager.get_related_tasks_titles()
        
        assert isinstance(titles, list)
        assert len(titles) == 4
        assert all(isinstance(title, str) for title in titles)

    def test_get_related_documents_titles(self, chat_manager):
        """Test get_related_documents_titles method."""
        titles = chat_manager.get_related_documents_titles()
        
        assert isinstance(titles, list)
        assert len(titles) == 4
        assert all(isinstance(title, str) for title in titles)


class TestChatManagerHistory:
    """Test ChatManager history methods."""

    @patch('src.role.chat_manager.ChatRepository')
    def test_chat_history(self, mock_repo_cls):
        """Test chat_history property."""
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = [["user", "assistant"]]
        mock_repo_cls.return_value = mock_repo
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        history = manager.chat_history()
        
        assert history == [["user", "assistant"]]
        mock_repo.get_chat_history.assert_called_once()


class TestChatManagerPrivateMethods:
    """Test ChatManager private methods."""

    @patch('src.role.chat_manager.ChatRepository')
    def test_add_user_query_to_chat_history(self, mock_repo_cls):
        """Test _add_user_query_to_chat_history method."""
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = []
        mock_repo.update_chat_history.return_value = None
        mock_repo_cls.return_value = mock_repo
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        manager._add_user_query_to_chat_history("test query")
        
        mock_repo.get_chat_history.assert_called()
        mock_repo.update_chat_history.assert_called_once()

    @patch('src.role.chat_manager.ChatRepository')
    def test_append_assistant_response_to_chat_history(self, mock_repo_cls):
        """Test _append_assistant_response_to_chat_history method."""
        mock_repo = MagicMock()
        mock_repo.get_chat_history.return_value = [["user", ""]]
        mock_repo.update_chat_history.return_value = None
        mock_repo_cls.return_value = mock_repo
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        manager._append_assistant_response_to_chat_history("chunk")
        
        mock_repo.get_chat_history.assert_called()
        mock_repo.update_chat_history.assert_called_once()

    @patch('src.role.chat_manager.ChatRepository')
    def test_convert_chat_history_to_chat_messages(self, mock_repo_cls):
        """Test _convert_chat_history_to_chat_messages method."""
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        chat_history = [["user1", "assistant1"], ["user2", ""]]
        result = manager._convert_chat_history_to_chat_messages(chat_history)
        
        assert len(result) == 3
        assert result[0].role == "user"
        assert result[0].content == "user1"
        assert result[1].role == "assistant"
        assert result[1].content == "assistant1"
        assert result[2].role == "user"
        assert result[2].content == "user2"

    @patch('src.role.chat_manager.ChatRepository')
    def test_convert_chat_history_to_chat_messages_empty(self, mock_repo_cls):
        """Test _convert_chat_history_to_chat_messages with empty history."""
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        
        manager = ChatManager(
            ui_info_log=MagicMock(),
            ui_error_log=MagicMock()
        )
        
        result = manager._convert_chat_history_to_chat_messages([])
        
        assert len(result) == 0
