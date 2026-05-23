
from chromadb import ingest

from src.chains.rag_chain import build_rag_chain
from src.vectorstore.store import load_store, collection_exists
from src.embeddings.embedder import get_embedder
from src.retrieval.retriever import build_retriever
from src.chains.rag_chain import build_rag_chain
from src.ingestion.ingest import build_vectorstore
from src.utils.common import get_project_root
from src.config.settings import VECTORSTORE_PATH
import os

# GLOBAL STATE (important)
VECTORSTORE = None
RAG_CHAIN = None

def initialize():
    global VECTORSTORE, RAG_CHAIN

    embeddings = get_embedder()
    persist_directory = VECTORSTORE_PATH

    # build ONLY if missing
    if (not os.path.exists(persist_directory) 
        or not os.listdir(persist_directory)
        or not collection_exists(persist_directory, embeddings)):
        
        input_path = get_project_root() / "data" / "raw"
        build_vectorstore(
            input_path=input_path,
            persist_directory=persist_directory,
            embeddings=embeddings
        )

    # load once
    VECTORSTORE = load_store(persist_directory, embeddings)

    retriever = build_retriever(VECTORSTORE)
    RAG_CHAIN = build_rag_chain(retriever)


def query(question: str):
    global RAG_CHAIN
    result = RAG_CHAIN(question)
    if isinstance(result, dict):
        # return result.get("answer", str(result))
        answer = result["result"]
        docs = result["source_documents"]
        return answer, docs
    return result