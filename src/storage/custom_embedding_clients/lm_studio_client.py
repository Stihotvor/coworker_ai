from typing import Any, List, Optional

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.bridge.pydantic import Field
from llama_index.core.callbacks.base import CallbackManager
from llama_index.core.constants import DEFAULT_EMBED_BATCH_SIZE


class LMStudioEmbedding(BaseEmbedding):
    """Class for LMStudio embeddings. Only if you need to generate embeddings manually."""

    base_url: str = Field(description="Base url the model is hosted by LMStudio")
    model_name: str = Field(description="The Ollama model to use.")
    embed_batch_size: int = Field(
        default=DEFAULT_EMBED_BATCH_SIZE,
        description="The batch size for embedding calls.",
        gt=0,
        le=2048,
    )

    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:1234",
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        super().__init__(  # type: ignore[call-arg]
            model_name=model_name,
            base_url=base_url,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,  # type: ignore[arg-type]
        )

    @classmethod
    def class_name(cls) -> str:
        return "LMStudioEmbedding"

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        return self.get_general_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """The asynchronous version of _get_query_embedding."""
        return self.get_general_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        return self.get_general_text_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronously get text embedding."""
        return self.get_general_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings."""
        embeddings_list: List[List[float]] = []
        for text in texts:
            embeddings = self.get_general_text_embedding(text)
            embeddings_list.append(embeddings)

        return embeddings_list

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Asynchronously get text embeddings."""
        return self._get_text_embeddings(texts)

    def get_general_text_embedding(
        self, prompt: str, dimensions: Optional[int] = None
    ) -> List[float]:
        """Get LMStudio embedding."""
        from openai import OpenAI

        client = OpenAI(base_url=self.base_url, api_key="lm-studio")
        prompt = prompt.replace("\n", " ")
        create_kwargs: dict[str, Any] = {"input": [prompt], "model": self.model_name}
        if dimensions is not None:
            create_kwargs["dimensions"] = dimensions
        response = client.embeddings.create(**create_kwargs)
        return response.data[0].embedding
