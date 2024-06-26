import gradio as gr

from src.api.main import app as api_app


class ProcessManager:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def remove_process(self, process):
        self.processes.remove(process)

    def get_processes(self):
        return self.processes


def process(user_query: str, submit: bool):
    process_manager = ProcessManager()
    chat_history = [
        ["Hello there!", "Hi, Yevhen! How can I help You?"],
        ["I'm looking for the billing transaction recalculation module, we developed few months ago.",
         "Sure! Recalculation is the process of turning back the transactions we have generateds some time ago. "
         "It seems to me, that the development was not completed. The last task moved to a 'Developed' stage was"
         " PART-4526 managed by Marcel D."]
    ]
    return chat_history


class CoworkerUI:
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def build_ui(self):
        with gr.Blocks() as blocks:
            self._build_row()
            self._init_submission()

        return blocks

    def _build_row(self):
        with gr.Row():
            self._build_left_column()
            self._build_right_column()

    def _build_left_column(self):
        with gr.Column(scale=3):
            # Outputs
            chat = gr.Chatbot(height=800, label="CoworkerAI")
            self.outputs.append(chat)

            # Inputs
            with gr.Row():
                user_query = gr.Textbox(scale=4, show_label=False)
                submit = gr.Button("Submit", scale=1, variant="primary")

                self.inputs.append(user_query)
                self.inputs.append(submit)

    def _build_right_column(self):
        # TODO: Add items dynamically
        tasks = [
            {'id': 'PART-4526', 'title': 'Some task A', 'status': 'To do'},
            {'id': 'PART-4525', 'title': 'Some task B', 'status': 'In progress'},
            {'id': 'PART-4524', 'title': 'Some task C', 'status': 'Release'},
            {'id': 'PART-4527', 'title': 'Some task D', 'status': 'Testing'}
        ]
        documents = [
            {'id': 'DOC-123', 'title': 'Recalculation design'},
            {'id': 'DOC-456', 'title': 'Billing rules setup'},
            {'id': 'DOC-789', 'title': 'Transaction table schema'},
            {'id': 'DOC-789', 'title': 'Activity report rules'},
        ]

        with gr.Column(scale=1):
            # Create a group of accordions in a list
            with gr.Group(visible=True):
                gr.Markdown('<h1 style="padding-left: 10px;">Related tasks</h1>', show_label=False)
                for task in tasks:
                    btn_text = f'{task["id"]} {task["title"]}'
                    task_btn = gr.Button(btn_text, elem_id=task["id"])
                    task_btn.click(lambda task_id=task["id"]: gr.Info(
                        f'Generating summary for the task {task_id}. Please, wait...'))

            with gr.Group(visible=True):
                gr.Markdown('<h1 style="padding-left: 10px;">Related documents</h1>', show_label=False)
                for document in documents:
                    btn_text = document["title"][:50]
                    document_btn = gr.Button(btn_text, elem_id=document["id"])
                    document_btn.click(lambda document_id=document["id"]: gr.Info(
                        f'Generating summary for the document {document_id}. Please, wait...'))


    def _init_submission(self):
        submit = self.inputs[-1]
        submit.click(process, inputs=self.inputs, outputs=self.outputs)


ui = CoworkerUI().build_ui()

app = gr.mount_gradio_app(api_app, ui, path="")
