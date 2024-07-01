from llama_index.llms.lmstudio import LMStudio
from llama_index.core.base.llms.types import ChatMessage, MessageRole

from src.role.prompt_repository.manager import SystemPrompt

llm = LMStudio(
    model_name="Meta-Llama-3-8B-Instruct-IQ3_M",
    # base_url="http://host.docker.internal:1234/v1",  # From docker
    base_url="http://127.0.0.1:1234/v1",  # Local
    temperature=0.5,
    timeout=300
)

response = llm.complete("Hey there, what is 2+2?")
print(str(response))

# use llm.stream_complete
response = llm.stream_complete("What is 7+3?")
for r in response:
    print(r.delta, end="")

#
# messages = [
#     ChatMessage(
#         role=MessageRole.SYSTEM,
#         content=SystemPrompt.DEFAULT.value,
#     ),
#     ChatMessage(
#         role=MessageRole.USER,
#         content="What is the significance of the number 42?",
#     ),
# ]
#
# response = llm.stream_chat(messages=messages)
# for r in response:
#     print(r.delta, end="")


from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def get_embedding(text, model="your-lm-studio-embedding-model"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


result = get_embedding("What is the significance of the number 42?")
print(result)