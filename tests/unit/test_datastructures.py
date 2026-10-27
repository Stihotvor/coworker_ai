"""Tests for datastructures module."""

import pytest
from src.role.datastructures import LLMConfig
from src.ui.datastructures import Task, TaskStatus, Document, RelatedTasks, RelatedDocuments


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


class TestTask:
    """Test cases for Task dataclass."""

    def test_task_creation(self):
        """Test Task creation with all fields."""
        task = Task(
            id="TASK-0001",
            title="Test Task",
            status=TaskStatus.TO_DO,
            responsible_person="test-user",
            context="Test context"
        )
        assert task.id == "TASK-0001"
        assert task.title == "Test Task"
        assert task.status == TaskStatus.TO_DO
        assert task.responsible_person == "test-user"
        assert task.context == "Test context"

    def test_task_creation_minimal(self):
        """Test Task creation with minimal fields."""
        task = Task(
            id="TASK-0001",
            title="Test Task",
            status=TaskStatus.NA
        )
        assert task.id == "TASK-0001"
        assert task.title == "Test Task"
        assert task.status == TaskStatus.NA
        assert task.responsible_person is None
        assert task.context is None

    def test_task_status_values(self):
        """Test all TaskStatus enum values."""
        statuses = [
            TaskStatus.TO_DO,
            TaskStatus.IN_PROGRESS,
            TaskStatus.DEVELOPED,
            TaskStatus.TESTED,
            TaskStatus.RELEASED,
            TaskStatus.NA
        ]
        for status in statuses:
            task = Task(id="1", title="test", status=status)
            assert task.status == status


class TestDocument:
    """Test cases for Document dataclass."""

    def test_document_creation(self):
        """Test Document creation."""
        doc = Document(
            id="DOC-0001",
            title="Test Document",
            context="Test content"
        )
        assert doc.id == "DOC-0001"
        assert doc.title == "Test Document"
        assert doc.context == "Test content"


class TestRelatedTasks:
    """Test cases for RelatedTasks dataclass."""

    def test_related_tasks_default_values(self):
        """Test RelatedTasks with default values."""
        related = RelatedTasks()
        assert related.task_1.id == "TASK-0000"
        assert related.task_1.title == "No data"
        assert related.task_1.status == TaskStatus.NA
        assert related.task_2.id == "TASK-0000"
        assert related.task_3.id == "TASK-0000"
        assert related.task_4.id == "TASK-0000"

    def test_related_tasks_custom_values(self):
        """Test RelatedTasks with custom values."""
        task1 = Task(id="TASK-0001", title="Task 1", status=TaskStatus.TO_DO)
        task2 = Task(id="TASK-0002", title="Task 2", status=TaskStatus.IN_PROGRESS)
        
        related = RelatedTasks(
            task_1=task1,
            task_2=task2
        )
        assert related.task_1.id == "TASK-0001"
        assert related.task_2.id == "TASK-0002"
        assert related.task_3.id == "TASK-0000"  # Default
        assert related.task_4.id == "TASK-0000"  # Default


class TestRelatedDocuments:
    """Test cases for RelatedDocuments dataclass."""

    def test_related_documents_default_values(self):
        """Test RelatedDocuments with default values."""
        related = RelatedDocuments()
        assert related.document_1.id == "DOC-0000"
        assert related.document_1.title == "No data"
        assert related.document_1.context == "No data"
        assert related.document_2.id == "DOC-0000"
        assert related.document_3.id == "DOC-0000"
        assert related.document_4.id == "DOC-0000"

    def test_related_documents_custom_values(self):
        """Test RelatedDocuments with custom values."""
        doc1 = Document(id="DOC-0001", title="Doc 1", context="Content 1")
        doc2 = Document(id="DOC-0002", title="Doc 2", context="Content 2")
        
        related = RelatedDocuments(
            document_1=doc1,
            document_2=doc2
        )
        assert related.document_1.id == "DOC-0001"
        assert related.document_2.id == "DOC-0002"
        assert related.document_3.id == "DOC-0000"  # Default
        assert related.document_4.id == "DOC-0000"  # Default
