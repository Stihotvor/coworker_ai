import logging
from typing import Type, Callable, Iterator

from llama_index.core.base.llms.types import ChatMessage

from src.storage.chat_repository import ChatRepository
from src.storage.vector_db import VectorStoreIndexManager
from src.ui.datastructures import RelatedTasks, RelatedDocuments, Task, TaskStatus, Document

log = logging.getLogger("storageLogger.chat_manager")


class ChatManager:
    """
    ChatManager class is responsible for managing the chat between the user and the AI assistant. It processes the
    user query, generates the response from the AI assistant, and updates the chat history. It also provides the
    functionality to list relevant tasks and documents to the user.

    Usage:
        chat = ChatManager(ui_info_log, ui_error_log)

        # Predict the response for the user query
        response = chat.predict("What do You know about task FITO-2311?")

        # Stream the chat response
        for chunk in response:
            # Print the whole chat with one more chunk
            print(chunk)

        # Call the property only after the response is generated
        for task in chat.related_tasks:
            print(task.title)

        # Call the property only after the response is generated
        for doc in chat.related_documents:
            print(doc.title)

        # Generate the task summary
        response = chat.generate_task_summary("FITO-2311")

        # Stream the chat response
        for chunk in response:
            # Print the whole chat with one more chunk
            print(chunk)

        # Resets the chat history, related tasks, and related documents
        chat.reset_chat_history()
    """

    def __init__(self,
                 ui_info_log: Callable,
                 ui_error_log: Callable,
                 chat_repository_cls: Type["ChatRepository"] = ChatRepository,
                 vector_store_index_cls: Type["VectorStoreIndexManager"] = VectorStoreIndexManager,
                 ):
        log.info("Initializing the ChatManager")
        self._ui_info_log = ui_info_log
        self._ui_error_log = ui_error_log
        self.chat_repository = chat_repository_cls()
        self._store = vector_store_index_cls()
        self._related_tasks = RelatedTasks()
        self._related_documents = RelatedDocuments()

        log.info("ChatManager is initialized")

    def reset_chat_history(self):
        """Reset the chat history, related tasks, and related documents."""
        # TODO: Reset documents, tasks
        # TODO: Add user session parameter
        log.debug("Resetting the chat history, related tasks, and related documents")
        self.chat_repository.reset_chat_history()
        self._ui_info_log("Chat history is reset")

    def reset_related_tasks(self):
        """Reset the related tasks."""
        # TODO: Add user session parameter
        log.info("Resetting the related tasks")
        self._related_tasks = RelatedTasks()
        log.info("Related tasks are reset")

    def reset_related_documents(self):
        """Reset the related documents."""
        log.info("Resetting the related documents")
        self._related_documents = RelatedDocuments()
        log.info("Related documents are reset")


    def reindex_documents(self):
        """Reindex the documents."""
        log.info("Re-indexing the documents")
        self._ui_info_log("Re-indexing the documents")
        self._store.reindex_documents()
        log.info("Documents are re-indexed")
        self._ui_info_log("Documents are re-indexed")

    def predict(self, user_query: str) -> Iterator[list[list[str]]]:
        """
        Predict the response for the user query. It generates the response from the AI assistant based on the user query
        and the chat history.
        """
        log.info(f"Predicting the response for the user query: {user_query[:10]}")
        # TODO: Add real documents and tasks to cache and clean after the chat cleaning
        # RFE: Add user session parameter
        # RFE: What to do between predicts? Reset the documents? Will it search again? Should I supply the nodes?
        # Pull out the task and doc titles
        task_titles = [getattr(self._related_tasks, f"task_{i}").title[:30] for i in range(1, 5)]

        doc_titles = [getattr(self._related_documents, f"document_{i}").title[:30] for i in range(1, 5)]

        if not user_query:
            self._ui_error_log("Please, provide a valid query.")
            return "", self.chat_repository.get_chat_history(), *task_titles, *doc_titles

        self._add_user_query_to_chat_history(user_query)

        # Grab the related docs from RAG
        converted_history = self._convert_chat_history_to_chat_messages(self.chat_repository.get_chat_history())

        chat_engine = self._store.get_chat_engine()
        llm_response = chat_engine.stream_chat(
            message=user_query,
            chat_history=converted_history
        )
        log.debug("LLM response is generated")

        related_task_names = set()
        related_doc_names = set()

        for node in llm_response.source_nodes:
            log.debug(f"Node document_type: {node.metadata["document_type"]}")
            if node.metadata["document_type"] == "tickets":
                related_task_names.add(node.metadata["file_name"])
            elif node.metadata["document_type"] == "documentation":
                related_doc_names.add(node.metadata["file_name"])

        # Truncate the sets to 4 items only
        related_task_names = list(related_task_names)[:4]
        related_doc_names = list(related_doc_names)[:4]

        # Update the related tasks 1-4, make sure if there is not enough related tasks, it is skipped
        for i, file_name in enumerate(related_task_names):
            related_task = Task(id=file_name, title=file_name.split(".")[0], status=TaskStatus.NA)
            setattr(self._related_tasks, f"task_{i + 1}", related_task)

        task_titles = [getattr(self._related_tasks, f"task_{i}").title[:30] for i in range(1, 5)]

        # Update the related documents 1-4
        for i, file_name in enumerate(related_doc_names):
            related_document = Document(id=file_name, title=file_name.split(".")[0], context="N/A")
            setattr(self._related_documents, f"document_{i + 1}", related_document)

        doc_titles = [getattr(self._related_documents, f"document_{i}").title[:30] for i in range(1, 5)]

        log.debug("Yielding the response")
        for chunk in llm_response.response_gen:
            self._append_assistant_response_to_chat_history(chunk)
            yield "", self.chat_repository.get_chat_history(), *task_titles, *doc_titles

        log.info("Response is yielded")

    @property
    def related_tasks(self) -> "RelatedTasks":
        """List of related tasks."""
        # TODO
        return RelatedTasks()

    @property
    def related_documents(self) -> "RelatedDocuments":
        """List of related documents."""
        # TODO
        return RelatedDocuments()

    def generate_task_summary(self, task_title_with_no: str):
        """Generate the task summary for the given task title."""
        # TODO
        pass

    def generate_document_summary(self, document_title_with_no: str):
        """Generate the document summary for the given document title."""
        # TODO
        pass

    def chat_history(self) -> list[list[str]]:
        """Get the chat history."""
        # TODO: Add user session
        log.info("Getting the chat history")
        return self.chat_repository.get_chat_history()

    def _add_user_query_to_chat_history(self, user_query: str) -> None:
        """Add the history record to the chat history."""
        log.debug(f"Adding the user query to the chat history: {user_query[:10]}")
        chat_history = self.chat_repository.get_chat_history()
        chat_history.append([user_query, ""])
        self.chat_repository.update_chat_history(chat_history)
        log.debug(f"User query is added to the chat history: {user_query[:10]}")

    def _append_assistant_response_to_chat_history(self, chunk: str) -> None:
        """Append the assistant response to the chat history."""
        chat_history = self.chat_repository.get_chat_history()
        chat_history[-1][1] += chunk
        self.chat_repository.update_chat_history(chat_history)

    def _convert_chat_history_to_chat_messages(self, chat_history: list[list[str]]) -> list[ChatMessage]:
        """Convert the chat history to the chat messages."""
        log.debug("Converting the chat history to the chat messages")
        chat_history_converted = []
        for user_message, assistant_message in chat_history:
            chat_history_converted.append(ChatMessage(role="user", content=user_message))

            if assistant_message:
                chat_history_converted.append(ChatMessage(role="assistant", content=assistant_message))

        log.debug("Chat history is converted to the chat messages")
        return chat_history_converted

# class OldChatManager:
#     def __init__(self,
#                  ui_info_log: Callable,
#                  ui_error_log: Callable,
#                  chat_repository_cls: Type["ChatRepository"] = ChatRepository,
#                  llm_client_cls: Type["LLMClient"] = LLMClient
#                  ):
#         self.ui_info_log = ui_info_log
#         self.ui_error_log = ui_error_log
#         self._chat_history = []
#         self._llm_client = llm_client_cls(config=LLM_CONFIG)
#
#     @property
#     def related_tasks(self) -> "RelatedTasks":
#         return RelatedTasks()
#
#     @property
#     def related_documents(self) -> "RelatedDocuments":
#         return RelatedDocuments()
#
#     @property
#     def chat_history(self) -> list[list[str]]:
#         return self._chat_history
#
#     def reset_chat_history(self):
#         self._chat_history = []
#
#     def generate_task_summary(self, task_title_with_no: str):
#         """I've had to hack as there is no clear way to pass arguments with .click()"""
#         task_no = task_title_with_no.split(".")[0]
#
#         if task_no not in ["1", "2", "3", "4"]:
#             self.ui_error_log("Invalid task number. Please, select a task from 1 to 4.")
#             return
#
#         task = getattr(self.related_tasks, f"task_{task_no}")
#         self.ui_info_log(f"Generating summary for the task {task.id}. Please, wait...")
#         # TODO: Implement the task summary generation
#
#     def generate_document_summary(self, document_title_with_no: str):
#         """I've had to hack as there is no clear way to pass arguments with .click()"""
#         doc_no = document_title_with_no.split(".")[0]
#
#         if doc_no not in ["1", "2", "3", "4"]:
#             self.ui_error_log("Invalid document number. Please, select a doc from 1 to 4.")
#             return
#
#         doc = getattr(self.related_documents, f"document_{doc_no}")
#         self.ui_info_log(f"Generating summary for the document {doc.id}. Please, wait...")
#         # TODO: Implement the task summary generation
#
#     def predict(self, user_query: str) -> Iterator[list[list[str]]]:
#         """
#         Generator function to process the user query with LLM. It yields the response in a form of a chat message
#         history. Each new iteration contains history of all messages up to this point. The latest message is updated
#         with the new characters returned from the LLM. Once the chat stream is finished, it returns the StopIteration.
#
#         Returns:
#             Iterator[list[list[str]]]: Chat message history in a format [..., [user_message, system_message], ...]
#         """
#         # Add the user query to the chat history
#         self.chat_history.append([user_query, ""])
#
#         tasks = [self.related_tasks.task_1, self.related_tasks.task_2,
#                  self.related_tasks.task_3, self.related_tasks.task_4]
#         task_titles = []
#         for i, task in enumerate(tasks):
#             task_titles.append(f"{i + 1}. {task.id} - {task.title[:30]}")
#
#         documents = [self.related_documents.document_1, self.related_documents.document_2,
#                      self.related_documents.document_3, self.related_documents.document_4]
#         doc_titles = []
#         for i, doc in enumerate(documents):
#             doc_titles.append(doc.title[:30])
#
#         assistant_role = SystemPrompt.COWORKER
#         additional_context = self._get_additional_context()
#         llm_response = self._llm_client.complete_chat(self._chat_history, assistant_role=assistant_role,
#                                                       additional_context=additional_context)
#
#         for chunk in llm_response:
#             self._chat_history[-1][1] += chunk
#             yield "", self._chat_history, *task_titles, *doc_titles
#
#     def _get_additional_context(self) -> str:
#         """Collect additional context from embeddings for each related task and document."""
#         context = ["Related tasks:"]
#         for task in [self.related_tasks.task_1, self.related_tasks.task_2,
#                      self.related_tasks.task_3, self.related_tasks.task_4]:
#             if task.status == TaskStatus.NA:
#                 continue
#
#             context.append(
#                 f"Task {task.id}. Task status: {task.status.value}. Responsible person: {task.responsible_person}. "
#                 f"Task context: {task.context}"
#             )
#
#         context.append("Related documents:")
#         for doc in [self.related_documents.document_1, self.related_documents.document_2,
#                     self.related_documents.document_3, self.related_documents.document_4]:
#             if not doc.context:
#                 continue
#
#             context.append(
#                 f"Document title {doc.title}. Document context: {doc.context}"
#             )
#
#         return "\n".join(context)
