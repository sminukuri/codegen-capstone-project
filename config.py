import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

STARCODER_BASE_MODEL = os.getenv("STARCODER_BASE_MODEL", "bigcode/starcoder2-3b")
QWEN_BASE_MODEL = os.getenv("QWEN_BASE_MODEL", "Qwen/Qwen2.5-Coder-3B-Instruct")
LLAMA_BASE_MODEL = os.getenv("LLAMA_BASE_MODEL", "Llama-3.1-8B-Instant")
HF_TOKEN = os.getenv("HF_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
FAST_API_URL = os.getenv("FAST_API_URL", "http://localhost:8000")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not set. Create a .env file with HF_TOKEN=your_token")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Create a .env file with GROQ_API_KEY=your_token")