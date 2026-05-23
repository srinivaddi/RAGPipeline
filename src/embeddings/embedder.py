
from langchain_ollama import OllamaEmbeddings
from src.config.settings import LOCAL_EMBEDDING_MODEL

def get_embedder():
    return OllamaEmbeddings(model=LOCAL_EMBEDDING_MODEL)
