from enum import Enum
from typing import Literal


def collect_prompt(file_name: str, prompt_type: Literal["system", "user"] = "system") -> str:
    """
    Collect the prompt from the .md file. Please, supply file_name without the extension.
    """
    # Open the .md file
    with open(f"src/role/prompt_repository/{prompt_type}/{file_name}.md", "r") as file:
        prompt = file.read()

    return prompt


# TODO: Load prompts to cache instead of memory or make it lazy
class SystemPrompt(Enum):
    """
    System prompts for the LLM.
    """
    DEFAULT = collect_prompt("default")
