import logging.config
from typing import Type

import gradio as gr

from src.role.chat_manager import ChatManager

logging.config.fileConfig('logging.ini')
log = logging.getLogger("uiLogger.main")


def build_ui(chat_manager_cls: Type["ChatManager"] = ChatManager):
    log.debug("Building the UI...")
    chat_manager = chat_manager_cls(ui_info_log=gr.Info, ui_error_log=gr.Warning)

    with gr.Blocks() as blocks:
        with gr.Row():
            with gr.Column(scale=3):
                chat = gr.Chatbot(height=800, label="CoworkerAI", placeholder="Start chatting with the bot!",
                                  value=chat_manager.chat_history)

                with gr.Row():
                    user_query = gr.Textbox(scale=4, show_label=False)
                    submit_btn = gr.Button("Submit", scale=1, variant="primary")
                    clear_btn = gr.ClearButton([user_query, chat], scale=1, variant="secondary")

            with gr.Column(scale=1):
                with gr.Group(visible=True):
                    gr.Markdown('<h1 style="padding-left: 10px;">Related tasks</h1>', show_label=False)

                    # TODO: Refresh the tasks and docs on each call
                    r_tasks = chat_manager.related_tasks
                    task_1_btn = gr.Button(f"1. {r_tasks.task_1.id} - {r_tasks.task_1.title[:30]}", )
                    # TODO: Implement the task summary generation with arguments to the function
                    task_1_btn.click(fn=chat_manager.generate_task_summary, inputs=[task_1_btn])
                    task_2_btn = gr.Button(f"2. {r_tasks.task_2.id} - {r_tasks.task_2.title[:30]}", )
                    task_2_btn.click(fn=chat_manager.generate_task_summary, inputs=[task_2_btn])
                    task_3_btn = gr.Button(f"3. {r_tasks.task_3.id} - {r_tasks.task_3.title[:30]}", )
                    task_3_btn.click(fn=chat_manager.generate_task_summary, inputs=[task_3_btn])
                    task_4_btn = gr.Button(f"4. {r_tasks.task_4.id} - {r_tasks.task_4.title[:30]}", )
                    task_4_btn.click(fn=chat_manager.generate_task_summary, inputs=[task_4_btn])

                with gr.Group(visible=True):
                    gr.Markdown('<h1 style="padding-left: 10px;">Related documents</h1>', show_label=False)
                    r_docs = chat_manager.related_documents
                    document_1_btn = gr.Button(f"1. {r_docs.document_1.title[:30]}")
                    document_1_btn.click(fn=chat_manager.generate_document_summary, inputs=[document_1_btn])
                    document_2_btn = gr.Button(f"2. {r_docs.document_2.title[:30]}")
                    document_2_btn.click(fn=chat_manager.generate_document_summary, inputs=[document_2_btn])
                    document_3_btn = gr.Button(f"3. {r_docs.document_3.title[:30]}")
                    document_3_btn.click(fn=chat_manager.generate_document_summary, inputs=[document_3_btn])
                    document_4_btn = gr.Button(f"4. {r_docs.document_4.title[:30]}")
                    document_4_btn.click(fn=chat_manager.generate_document_summary, inputs=[document_4_btn])

                reindex_doc_btn = gr.Button("Reindex documents")
        inputs = [user_query]
        outputs = [user_query, chat, task_1_btn, task_2_btn, task_3_btn, task_4_btn,
                   document_1_btn, document_2_btn, document_3_btn, document_4_btn]

        user_query.submit(chat_manager.predict, inputs=inputs, outputs=outputs)
        submit_btn.click(chat_manager.predict, inputs=inputs, outputs=outputs)
        clear_btn.click(chat_manager.reset_chat_history)
        reindex_doc_btn.click(chat_manager.reindex_documents)

    return blocks
