from typing import List, Iterator, Optional

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.lmstudio import LMStudio

from src.role.datastructures import LLMConfig
from src.role.prompt_repository.prompt_builder import SystemPrompt


class LLMClient:

    def __init__(self, config: "LLMConfig"):
        self.config = config
        self._client = self._get_client()

    def complete_chat(self, chat: List[List[str | None]], assistant_role: "SystemPrompt" = SystemPrompt.DEFAULT,
                      additional_context: Optional[str] = None) -> Iterator[str]:
        """
        Complete the chat with the LLM model response. Format of the chat: [[user_query, llm_response], ...]
        """
        chat_messages = self._convert_chat_to_chat_messages(chat, assistant_role, additional_context)
        response = self._client.stream_chat(chat_messages)
        for r in response:
            print(r.delta, end="")
            yield r.delta

    def _convert_chat_to_chat_messages(self, chat: List[List[str | None]], assistant_role: "SystemPrompt",
                                       additional_context: Optional[str] = None) -> List[ChatMessage]:
        messages = self._get_system_prompt(assistant_role, additional_context)
        for message_pair in chat:
            if message_pair[0]:
                messages.append(ChatMessage(content=message_pair[0], role=MessageRole.USER))

            if message_pair[1]:
                messages.append(ChatMessage(content=message_pair[1], role=MessageRole.ASSISTANT))
        return messages

    def _get_client(self) -> LMStudio:
        return LMStudio(
            model_name=self.config.model_name,
            temperature=self.config.temperature,
            base_url=self.config.completions_url,
        )

    def _get_system_prompt(self, assistant_role: "SystemPrompt", additional_context: Optional[str] = None) -> List[
        ChatMessage]:
        context = assistant_role.value
        if additional_context:
            context += f"\nAdditional context:\n{additional_context}"
        return [ChatMessage(content=context, role=MessageRole.SYSTEM)]
