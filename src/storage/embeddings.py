from llama_index.llms.lmstudio import LMStudio

from src.storage.custom_embedding_clients.lm_studio_client import LMStudioEmbedding

llm = LMStudio(
    model_name="Meta-Llama-3-8B-Instruct-IQ3_M",
    # base_url="http://host.docker.internal:1234/v1",  # From docker
    base_url="http://127.0.0.1:1234/v1",  # Local
    temperature=0.5,
    timeout=300
)


from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def get_embedding(text, model="all-MiniLM-L6-v2-ggml-model-f16"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


result = get_embedding("What is the significance of the number 42?")
print(len(result))
print(result)



embed_model = LMStudioEmbedding(
    base_url="http://localhost:1234/v1",
    model_name="all-MiniLM-L6-v2-ggml-model-f16"
)
pass_embedding = embed_model.get_general_text_embedding("What is the significance of the number 42?")
print(len(pass_embedding))
print(pass_embedding)