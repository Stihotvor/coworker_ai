import logging
import re
from typing import List

from llama_index.core.schema import TransformComponent, BaseNode

log = logging.getLogger("storageLogger.custom_transformations")


class TextCleaner(TransformComponent):
    def __call__(self, nodes: List["BaseNode"], **kwargs) -> List["BaseNode"]:
        log.info("Cleaning text")
        for node in nodes:
            node.text = re.sub(r"[^0-9A-Za-z ]", "", node.text)
        return nodes


class DocumentTypeToMetadata(TransformComponent):
    """
    Transform component to add metadata to the document nodes based on the document type.
    """

    def __call__(self, nodes: List["BaseNode"], **kwargs) -> List["BaseNode"]:
        log.info(f"Adding metadata to nodes for document type: {kwargs['document_type']}")
        for node in nodes:
            node.metadata["document_type"] = kwargs["document_type"]
        return nodes
