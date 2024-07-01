import inspect
from typing import Iterator, List

import gradio as gr
from gradio import processing_utils

from src.api.main import app as api_app
from src.ui.datastructures import RelatedTasks, RelatedDocuments


# Save the original function
original_hash_file = processing_utils.save_file_to_cache

def new_save_file_to_cache(file_path, cache_dir):
    # Print the arguments
    print(f"File path: {file_path}")
    print(f"Cache directory: {cache_dir}")

    # Print arguments of the caller function
    caller_frame = inspect.currentframe().f_back
    caller_frame_info = inspect.getframeinfo(caller_frame)
    print(f"Caller function: {caller_frame_info.function}")
    print(f"Caller arguments: {caller_frame.f_locals}")

    # Print caller of caller function
    caller_of_caller_frame = caller_frame.f_back
    caller_of_caller_frame_info = inspect.getframeinfo(caller_of_caller_frame)
    print(f"Caller of caller function: {caller_of_caller_frame_info.function}")
    print(f"Caller of caller arguments: {caller_of_caller_frame.f_locals}")

    # Print caller of caller of caller function
    caller_of_caller_of_caller_frame = caller_of_caller_frame.f_back
    caller_of_caller_of_caller_frame_info = inspect.getframeinfo(caller_of_caller_of_caller_frame)
    print(f"Caller of caller of caller function: {caller_of_caller_of_caller_frame_info.function}")
    print(f"Caller of caller of caller arguments: {caller_of_caller_of_caller_frame.f_locals}")

    # Print caller of caller of caller of caller function
    caller_of_caller_of_caller_of_caller_frame = caller_of_caller_of_caller_frame.f_back
    caller_of_caller_of_caller_of_caller_frame_info = inspect.getframeinfo(caller_of_caller_of_caller_of_caller_frame)
    print(f"Caller of caller of caller of caller function: {caller_of_caller_of_caller_of_caller_frame_info.function}")
    print(f"Caller of caller of caller of caller arguments: {caller_of_caller_of_caller_of_caller_frame.f_locals}")


    # Call the original function
    return original_hash_file(file_path, cache_dir)



# Replace the original function with the new function
processing_utils.save_file_to_cache = new_save_file_to_cache


class ChatManager:
    def __init__(self):
        self.chat_history = [["", "How can I help You?"]]

    def process_user_query(self, user_query: str) -> Iterator[list[list[str]]]:
        """
        Generator function to process the user query with LLM. It yields the response in a form of a chat message
        history. Each new iteration contains history of all messages up to this point. The latest message is updated
        with the new characters returned from the LLM. Once the chat stream is finished, it returns the StopIteration.

        Returns:
            Iterator[list[list[str]]]: Chat message history in a format [..., [user_message, system_message], ...]
        """
        # Add the user query to the chat history
        self.chat_history.append([user_query, ""])

        # Process the user query with LLM
        test_system_message = "Hello there!"

        # Add the system message to the chat history (we will have an LLM iterator here)
        for chunk in test_system_message.split():
            self.chat_history[-1][1] += chunk + " "
            print(self.chat_history)
            yield self.chat_history

    def process_user_query_once(self, user_query: str) -> List[List[str]]:
        """
        Process the user query once and return the chat history
        """
        self.chat_history.append([user_query, "Hello there! How are you doing today?"])
        return self.chat_history


# Override the default Gradio Blocks class to add

class CoworkerUI:
    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._related_tasks = RelatedTasks()
        self._related_documents = RelatedDocuments()

        # TODO: Add chat per user
        self._chat = ChatManager()

    def process_query(self, user_query: str, *args, **kwargs) -> Iterator[List[List[str]]] | List[List[str]]:
        """
        Processing wrapper. Handles exceptions coming from Chat Manager
        """
        if user_query:
            try:
                return self._chat.process_user_query(user_query=user_query)
                # TODO: Add more exception handling
            except Exception as e:
                # Show warning message
                gr.Warning(message=str(e)[:50])

            return self._chat.chat_history

    def process_query_once(self, user_query: str, *args, **kwargs) -> List[List[str]]:
        """
        Processing wrapper. Handles exceptions coming from Chat Manager
        """
        if user_query:
            try:
                return self._chat.process_user_query_once(user_query=user_query)
                # TODO: Add more exception handling
            except Exception as e:
                # Show warning message
                gr.Warning(message=str(e)[:50])

            return [[]]

    def build_ui(self) -> gr.Blocks:
        with gr.Blocks() as blocks:
            with gr.Row():
                with gr.Column(scale=3):
                    chat = gr.Chatbot(height=800, label="CoworkerAI", value=[["", "How can I help You?"]])
                    self._outputs.append(chat)

                    with gr.Row():
                        user_query = gr.Textbox(scale=4, show_label=False)
                        self._inputs.append(user_query)

                        submit_btn = gr.Button("Submit", scale=1, variant="primary")
                        self._inputs.append(submit_btn)
                        submit_btn.click(self.process_query, inputs=self._inputs, outputs=self._outputs)

                        gr.ClearButton([user_query, chat], scale=1, variant="secondary")

                with gr.Column(scale=1):
                    self._build_right_column()

        return blocks

    def _build_right_column(self):
        # Related tasks
        with gr.Group(visible=True):
            gr.Markdown('<h1 style="padding-left: 10px;">Related tasks</h1>', show_label=False)

            for i in range(1, 5):
                task = getattr(self._related_tasks, f"task_{i}")
                btn_text = f'{task.id} {task.title}'
                task_btn = gr.Button(btn_text, elem_id=task.id)

                # TODO: Add a click event
                task_btn.click(lambda task_id=task.id: gr.Info(
                    f'Generating summary for the task {task_id}. Please, wait...'))

            # Related documents
        with gr.Group(visible=True):
            gr.Markdown('<h1 style="padding-left: 10px;">Related documents</h1>', show_label=False)
            for i in range(1, 5):
                document = getattr(self._related_documents, f"document_{i}")
                btn_text = document.title[:50]
                document_btn = gr.Button(btn_text, elem_id=document.id)

                # TODO: Add a click event
                document_btn.click(lambda document_id=document.id: gr.Info(
                    f'Generating summary for the document {document_id}. Please, wait...'))


app = gr.mount_gradio_app(app=api_app, blocks=CoworkerUI().build_ui(), path="")
