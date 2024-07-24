import gradio as gr
from src.ui.main import build_ui


def app():
    import uvicorn
    from src.api.main import app as api_app
    app = gr.mount_gradio_app(app=api_app, blocks=build_ui(), path="")
    uvicorn.run(app, host="0.0.0.0", port=8010)
