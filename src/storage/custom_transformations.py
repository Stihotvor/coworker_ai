import logging
import re
from typing import Any, Sequence

from llama_index.core.schema import BaseNode, TransformComponent

log = logging.getLogger("storageLogger.custom_transformations")


class TextCleaner(TransformComponent):
    def __call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> Sequence[BaseNode]:
        log.info("Cleaning text")
        for node in nodes:
            node.text = re.sub(r"[^0-9A-Za-z ]", "", node.text)  # type: ignore[attr-defined]
        return nodes


class DocumentTypeToMetadata(TransformComponent):
    """
    Transform component to add metadata to the document nodes based on the document type.
    """

    def __call__(self, nodes: Sequence[BaseNode], **kwargs: Any) -> Sequence[BaseNode]:
        doc_type = kwargs.get("document_type", "unknown")
        log.info(f"Adding metadata to nodes for document type: {doc_type}")
        for node in nodes:
            node.metadata["document_type"] = doc_type
        return nodes
