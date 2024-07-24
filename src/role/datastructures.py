from dataclasses import dataclass


@dataclass
class LLMConfig:
    model_name: str
    max_tokens: int
    temperature: float
    stream: bool
    completions_url: str
