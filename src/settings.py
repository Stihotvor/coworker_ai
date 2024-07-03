from src.role.datastructures import LLMConfig

LLM_CONFIG = LLMConfig(
        model_name="mistral-7b-instruct-v0.1.Q2_K",
        max_tokens=-1,
        temperature=0.4,
        stream=True,
        completions_url="http://host.docker.internal:1234/v1",
    )