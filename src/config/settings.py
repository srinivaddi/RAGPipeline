
from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "qwen3-embedding:8b")

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "gemma4:e4b")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.5))

VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./vectorstoredb")

CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "SEMANTIC_THEN_RECURSIVE")
CHUNK_TYPE = os.getenv("CHUNK_TYPE", "HYBRID")
MINIMUM_CHUNK_SIZE = int(os.getenv("MINIMUM_CHUNK_SIZE", 200))
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 1))             

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))
LENGTH_FUNCTION = os.getenv("LENGTH_FUNCTION", "token_length")

BREAKPOINT_THRESHOLD_TYPE = os.getenv("BREAKPOINT_THRESHOLD_TYPE", "percentile")
BREAKPOINT_THRESHOLD_AMOUNT = int(os.getenv("BREAKPOINT_THRESHOLD_AMOUNT", "95"))

RAG_PROMPT= os.getenv("RAG_PROMPT", "RAG_PROMPT_GROUNDED")