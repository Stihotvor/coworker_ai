import gradio as gr
from src.api.main import app as api_app
from src.ui.main import build_ui

app = gr.mount_gradio_app(app=api_app, blocks=build_ui(), path="")