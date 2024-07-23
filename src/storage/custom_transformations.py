import re
from typing import List

from llama_index.core.schema import TransformComponent, BaseNode


class TextCleaner(TransformComponent):
    def __call__(self, nodes: List["BaseNode"], **kwargs) -> List["BaseNode"]:
        for node in nodes:
            node.text = re.sub(r"[^0-9A-Za-z ]", "", node.text)
        return nodes


class DocumentTypeToMetadata(TransformComponent):
    """
    Transform component to add metadata to the document nodes based on the document type.
    """
    def __call__(self, nodes: List["BaseNode"], **kwargs) -> List["BaseNode"]:
        for node in nodes:
            node.metadata["document_type"] = kwargs["document_type"]
        return nodes