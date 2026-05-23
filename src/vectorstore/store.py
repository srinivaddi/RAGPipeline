from langchain_chroma import Chroma

from src.config.settings import CHUNKING_STRATEGY

def create_store(docs, embeddings, persist_directory="./chroma_db"):
    """Creates and saves a Chroma vector store to a directory."""
    return Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )

def load_store(path, embeddings):
    """Loads an existing Chroma vector store from a directory."""

    collection_name=CHUNKING_STRATEGY.lower()
    return Chroma(
        persist_directory=path, 
        embedding_function=embeddings,
        collection_name=collection_name  # specify collection name if needed
    )

def collection_exists(persist_directory, embeddings):
    try:
        collection_name=CHUNKING_STRATEGY.lower()
        # collection_name="DEFAULT".lower()

        db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name=collection_name,
        )

        # Try to query metadata
        count = db._collection.count()

        return count > 0

    except Exception:
        return False