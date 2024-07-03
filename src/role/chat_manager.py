from typing import Type, Callable, Iterator

from src.role.llm_client import LLMClient
from src.role.prompt_repository.prompt_builder import SystemPrompt
from src.settings import LLM_CONFIG
from src.storage.chats import ChatRepository
from src.ui.datastructures import RelatedTasks, RelatedDocuments, TaskStatus


class ChatManager:
    def __init__(self,
                 ui_info_log: Callable,
                 ui_error_log: Callable,
                 chat_repository_cls: Type["ChatRepository"] = ChatRepository,
                 llm_client_cls: Type["LLMClient"] = LLMClient
                 ):
        self.ui_info_log = ui_info_log
        self.ui_error_log = ui_error_log
        self._chat_history = []
        self._llm_client = llm_client_cls(config=LLM_CONFIG)

    @property
    def related_tasks(self) -> "RelatedTasks":
        return RelatedTasks()

    @property
    def related_documents(self) -> "RelatedDocuments":
        return RelatedDocuments()

    @property
    def chat_history(self) -> list[list[str]]:
        return self._chat_history

    def reset_chat_history(self):
        self._chat_history = []

    def generate_task_summary(self, task_title_with_no: str):
        """I've had to hack as there is no clear way to pass arguments with .click()"""
        task_no = task_title_with_no.split(".")[0]

        if task_no not in ["1", "2", "3", "4"]:
            self.ui_error_log("Invalid task number. Please, select a task from 1 to 4.")
            return

        task = getattr(self.related_tasks, f"task_{task_no}")
        self.ui_info_log(f"Generating summary for the task {task.id}. Please, wait...")
        # TODO: Implement the task summary generation

    def generate_document_summary(self, document_title_with_no: str):
        """I've had to hack as there is no clear way to pass arguments with .click()"""
        doc_no = document_title_with_no.split(".")[0]

        if doc_no not in ["1", "2", "3", "4"]:
            self.ui_error_log("Invalid document number. Please, select a doc from 1 to 4.")
            return

        doc = getattr(self.related_documents, f"document_{doc_no}")
        self.ui_info_log(f"Generating summary for the document {doc.id}. Please, wait...")
        # TODO: Implement the task summary generation

    def predict(self, user_query: str) -> Iterator[list[list[str]]]:
        """
        Generator function to process the user query with LLM. It yields the response in a form of a chat message
        history. Each new iteration contains history of all messages up to this point. The latest message is updated
        with the new characters returned from the LLM. Once the chat stream is finished, it returns the StopIteration.

        Returns:
            Iterator[list[list[str]]]: Chat message history in a format [..., [user_message, system_message], ...]
        """
        # Add the user query to the chat history
        self.chat_history.append([user_query, ""])

        tasks = [self.related_tasks.task_1, self.related_tasks.task_2,
                 self.related_tasks.task_3, self.related_tasks.task_4]
        task_titles = []
        for i, task in enumerate(tasks):
            task_titles.append(f"{i + 1}. {task.id} - {task.title[:30]}")

        documents = [self.related_documents.document_1, self.related_documents.document_2,
                     self.related_documents.document_3, self.related_documents.document_4]
        doc_titles = []
        for i, doc in enumerate(documents):
            doc_titles.append(doc.title[:30])

        assistant_role = SystemPrompt.COWORKER
        additional_context = self._get_additional_context()
        llm_response = self._llm_client.complete_chat(self._chat_history, assistant_role=assistant_role,
                                                      additional_context=additional_context)

        for chunk in llm_response:
            self._chat_history[-1][1] += chunk
            yield "", self._chat_history, *task_titles, *doc_titles

    def _get_additional_context(self) -> str:
        """Collect additional context from embeddings for each related task and document."""
        context = ["Related tasks:"]
        for task in [self.related_tasks.task_1, self.related_tasks.task_2,
                     self.related_tasks.task_3, self.related_tasks.task_4]:
            if task.status == TaskStatus.NA:
                continue

            context.append(
                f"Task {task.id}. Task status: {task.status.value}. Responsible person: {task.responsible_person}. "
                f"Task context: {task.context}"
            )

        context.append("Related documents:")
        for doc in [self.related_documents.document_1, self.related_documents.document_2,
                    self.related_documents.document_3, self.related_documents.document_4]:
            if not doc.context:
                continue

            context.append(
                f"Document title {doc.title}. Document context: {doc.context}"
            )

        return "\n".join(context)