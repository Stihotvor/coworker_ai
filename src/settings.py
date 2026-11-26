from typing import Any

from llama_index.core import Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.llms.lmstudio import LMStudio

from src.storage.custom_embedding_clients.lm_studio_client import LMStudioEmbedding


def init_llm_config(settings: Any) -> None:
    settings.llm = LMStudio(
        model_name="TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q2_K.gguf",
        base_url="http://host.docker.internal:1234/v1",
        temperature=0.5,
        timeout=600,
        request_timeout=600,
    )


def init_embedding_config(settings: Any) -> None:
    settings.embed_model = LMStudioEmbedding(
        base_url="http://host.docker.internal:1234/v1",
        model_name="all-MiniLM-L6-v2-ggml-model-f16",
    )


def init_text_splitter(settings: Any) -> None:
    settings.text_splitter = SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=95,
        embed_model=settings.embed_model,
    )


def init_settings(settings: Any = Settings) -> None:
    init_llm_config(settings)
    init_embedding_config(settings)
    init_text_splitter(settings)
