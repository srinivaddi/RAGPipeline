import os
from pathlib import Path

from src.ingestion.loader import load_documents
from src.ingestion.splitter import split_documents
from src.config.settings import CHUNKING_STRATEGY

from langchain_chroma import Chroma

def build_vectorstore(
    input_path: str = "./data",
    persist_directory: str = "./vectorstoredb",
    embeddings = None
):
    """
    MAIN ingestion pipeline:
    1. Load PDFs
    2. Split into chunks
    3. Embed + store in Chroma
    """

    print("📂 Loading documents...")
    docs = load_documents(input_path)

    print(f"✅ Loaded {len(docs)} documents")

    print("✂️ Splitting documents...")
    chunks = split_documents(docs, embeddings)

    print(f"✅ Created {len(chunks)} chunks")

    print("💾 Creating vectorstore...")

    collection_name=CHUNKING_STRATEGY.lower()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )

    # Persist to disk
    if hasattr(vectorstore, "persist"):
        vectorstore.persist()

    print("✅ Vectorstore saved!")

    return vectorstore