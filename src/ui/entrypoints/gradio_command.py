from src.ui.main import build_ui

blocks = build_ui()


def app():
    # demo.queue()
    blocks.launch(server_port=8010, server_name="0.0.0.0", share=True)
