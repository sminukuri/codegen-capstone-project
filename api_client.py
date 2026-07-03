import requests
from config import FAST_API_URL 
from pydantic import BaseModel

class Request(BaseModel):
    query: str
    source_language: str
    target_language: str
    source_code: str
    output_code: str   

def generate_code(query: str) -> str:
    """
    Generate code using the FastAPI endpoint.

    Args:
        query (str): The query to send to the FastAPI endpoint.

    Returns:
        str: The generated code from the FastAPI response.
    """
    try:
        request_obj = Request(query=query, source_language="", target_language="", source_code="", output_code="")
        response = requests.post(f"{FAST_API_URL}/generate", json=request_obj.model_dump())
        response.raise_for_status()  # Raise an error for bad responses
        return str(response.json())
    except requests.RequestException as e:
        print(f"Error during request to FastAPI: {e}")
        return ""
    

def translate_code(source_code: str, source_language: str, target_language: str) -> str:
    """
    Translate code using the FastAPI endpoint.

    Args:
        source_code (str): The source code to translate.
        source_language (str): The language of the source code.
        target_language (str): The target language for translation.

    Returns:
        str: The translated code from the FastAPI response.
    """
    try:
        request_obj = Request(query="", source_language=source_language, target_language=target_language, source_code=source_code, output_code="")
        response = requests.post(
            f"{FAST_API_URL}/translate",
            json=request_obj.model_dump()
        )
        response.raise_for_status()  # Raise an error for bad responses
        return str(response.json())
    except requests.RequestException as e:
        print(f"Error during request to FastAPI: {e}")
        return ""

def explain_code(code: str) -> str:
    """
    Explain code using the FastAPI endpoint.

    Args:
        code (str): The code to explain.

    Returns:
        str: The explanation of the code from the FastAPI response.
    """
    try:
        request_obj = Request(query="", source_language="", target_language="", source_code="", output_code=code)
        response = requests.post(f"{FAST_API_URL}/explain", json=request_obj.model_dump())
        response.raise_for_status()  # Raise an error for bad responses
        return str(response.json())
    except requests.RequestException as e:
        print(f"Error during request to FastAPI: {e}")
        return ""    