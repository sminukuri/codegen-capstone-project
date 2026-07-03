
from typing import Any
from typing import Any

from state import AgentState
from api_client import generate_code, translate_code

def generate(state: AgentState) -> str:
    return generate_code(state.user_query)

def translate(state: AgentState) -> str:
    router_output = state.router
    if (
        router_output.source_code is None
        or router_output.source_language is None
        or router_output.target_language is None
    ):
        raise ValueError(
            "Router output must include source_code, source_language, and target_language for translation"
        )
    return translate_code(
        router_output.source_code,
        router_output.source_language,
        router_output.target_language,
    )