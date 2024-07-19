import re
from typing import List

from llama_index.core.schema import TransformComponent, BaseNode


class TextCleaner(TransformComponent):
    def __call__(self, nodes: List["BaseNode"], **kwargs) -> List["BaseNode"]:
        for node in nodes:
            node.text = re.sub(r"[^0-9A-Za-z ]", "", node.text)
        return nodes