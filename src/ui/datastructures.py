from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DEVELOPED = "developed"
    TESTED = "tested"
    RELEASED = "released"
    NA = "n/a"


@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus


@dataclass
class RelatedTasks:
    task_1: Task = field(default_factory=lambda: Task(id="TASK-0000", title="No data", status=TaskStatus.NA))
    task_2: Task = field(default_factory=lambda: Task(id="TASK-0000", title="No data", status=TaskStatus.NA))
    task_3: Task = field(default_factory=lambda: Task(id="TASK-0000", title="No data", status=TaskStatus.NA))
    task_4: Task = field(default_factory=lambda: Task(id="TASK-0000", title="No data", status=TaskStatus.NA))


@dataclass
class Document:
    id: str
    title: str


@dataclass
class RelatedDocuments:
    document_1: Document = field(default_factory=lambda: Document(id="DOC-0000", title="No data"))
    document_2: Document = field(default_factory=lambda: Document(id="DOC-0000", title="No data"))
    document_3: Document = field(default_factory=lambda: Document(id="DOC-0000", title="No data"))
    document_4: Document = field(default_factory=lambda: Document(id="DOC-0000", title="No data"))
