"""Unit tests for UI datastructures module."""

import pytest

from src.ui.datastructures import (
    Task,
    TaskStatus,
    Document,
    RelatedTasks,
    RelatedDocuments
)


class TestTaskStatus:
    """Test cases for TaskStatus enum."""

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
        
        values = [
            "to_do",
            "in_progress",
            "developed",
            "tested",
            "released",
            "n/a"
        ]
        
        for status, value in zip(statuses, values):
            assert status.value == value

    def test_task_status_unique(self):
        """Test that all TaskStatus values are unique."""
        values = [s.value for s in TaskStatus]
        assert len(values) == len(set(values))


class TestTask:
    """Test cases for Task dataclass."""

    def test_task_all_fields(self):
        """Test Task with all fields."""
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

    def test_task_minimal_fields(self):
        """Test Task with minimal required fields."""
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

    def test_task_equality(self):
        """Test Task equality comparison."""
        task1 = Task(
            id="TASK-0001",
            title="Test Task",
            status=TaskStatus.TO_DO
        )
        task2 = Task(
            id="TASK-0001",
            title="Test Task",
            status=TaskStatus.TO_DO
        )
        
        assert task1 == task2

    def test_task_inequality(self):
        """Test Task inequality comparison."""
        task1 = Task(
            id="TASK-0001",
            title="Test Task",
            status=TaskStatus.TO_DO
        )
        task2 = Task(
            id="TASK-0002",
            title="Test Task",
            status=TaskStatus.TO_DO
        )
        
        assert task1 != task2


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

    def test_document_equality(self):
        """Test Document equality comparison."""
        doc1 = Document(
            id="DOC-0001",
            title="Test Document",
            context="Test content"
        )
        doc2 = Document(
            id="DOC-0001",
            title="Test Document",
            context="Test content"
        )
        
        assert doc1 == doc2

    def test_document_inequality(self):
        """Test Document inequality comparison."""
        doc1 = Document(
            id="DOC-0001",
            title="Test Document",
            context="Test content"
        )
        doc2 = Document(
            id="DOC-0002",
            title="Test Document",
            context="Test content"
        )
        
        assert doc1 != doc2


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
        task3 = Task(id="TASK-0003", title="Task 3", status=TaskStatus.DEVELOPED)
        task4 = Task(id="TASK-0004", title="Task 4", status=TaskStatus.TESTED)
        
        related = RelatedTasks(
            task_1=task1,
            task_2=task2,
            task_3=task3,
            task_4=task4
        )
        
        assert related.task_1 == task1
        assert related.task_2 == task2
        assert related.task_3 == task3
        assert related.task_4 == task4

    def test_related_tasks_partial_custom_values(self):
        """Test RelatedTasks with partial custom values."""
        task1 = Task(id="TASK-0001", title="Task 1", status=TaskStatus.TO_DO)
        
        related = RelatedTasks(task_1=task1)
        
        assert related.task_1 == task1
        assert related.task_2.id == "TASK-0000"  # Default
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
        doc3 = Document(id="DOC-0003", title="Doc 3", context="Content 3")
        doc4 = Document(id="DOC-0004", title="Doc 4", context="Content 4")
        
        related = RelatedDocuments(
            document_1=doc1,
            document_2=doc2,
            document_3=doc3,
            document_4=doc4
        )
        
        assert related.document_1 == doc1
        assert related.document_2 == doc2
        assert related.document_3 == doc3
        assert related.document_4 == doc4

    def test_related_documents_partial_custom_values(self):
        """Test RelatedDocuments with partial custom values."""
        doc1 = Document(id="DOC-0001", title="Doc 1", context="Content 1")
        
        related = RelatedDocuments(document_1=doc1)
        
        assert related.document_1 == doc1
        assert related.document_2.id == "DOC-0000"  # Default
        assert related.document_3.id == "DOC-0000"  # Default
        assert related.document_4.id == "DOC-0000"  # Default
