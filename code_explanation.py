from typing import Any

from click import prompt
from pydantic import SecretStr
from typer import prompt

from state import AgentState
from config import GROQ_API_KEY, QWEN_BASE_MODEL
from langchain.messages import AIMessage
from langchain_groq import ChatGroq
from api_client import explain_code


def explain(state: AgentState) -> str:
    
    return explain_code(state["output_code"])