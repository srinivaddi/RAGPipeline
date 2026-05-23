# splitter.py
from __future__ import annotations

from email.mime import text
from typing import List

from langchain import embeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import re
import tiktoken
from src.config.settings import CHUNKING_STRATEGY, CHUNK_TYPE, CHUNK_SIZE, CHUNK_OVERLAP, \
                                BREAKPOINT_THRESHOLD_AMOUNT, BREAKPOINT_THRESHOLD_TYPE, LENGTH_FUNCTION, MINIMUM_CHUNK_SIZE, BUFFER_SIZE

def token_length(text: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return len(tokenizer.encode(text))

def split_documents(
    docs: List[Document],
    embeddings = None,
) -> List[Document]:
    """
    Split Documents into smaller chunks for embedding + retrieval.
    """
    
    chunks = []
    if CHUNKING_STRATEGY == "RECURSIVE_CHARACTER":
        # for books, novels, stories, conversational text where meaning is continuous, not segmented by structure, gradual transitions, entity-driven
        chunks = build_splitter_recursive().split_documents(docs)
    elif CHUNKING_STRATEGY == "SEMANTIC":
        # Use for manuals, documentation, FAQs, structured text, clear topic shifts, independent sections
        docs = split_by_chapter(docs)
        # later try split by section, subsection, etc. based on regex patterns and structure awareness
        chunks = build_splitter_semantic(embeddings).split_documents(docs)
    elif CHUNKING_STRATEGY == "SEMANTIC_THEN_RECURSIVE":
        docs = split_by_chapter(docs)
        # later try split by section, subsection, etc. based on regex patterns and structure awareness
        semantic_docs = build_splitter_semantic(embeddings).split_documents(docs)
        # chunks = build_splitter_recursive().split_documents(semantic_docs)
        
        for doc in semantic_docs:
            if len(doc.page_content) > 800:
                chunks.extend(build_splitter_recursive().split_documents([doc]))
            else:
                chunks.append(doc)
    
    return chunk_metadata(chunks)

def chunk_metadata(chunks):
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "position": i, 
            "chunk_id": f"{i}",

            # pipeline trace
            "chunking_strategy": CHUNKING_STRATEGY.strip().lower(),

            # type indicator
            "chunk_type": CHUNK_TYPE.strip().lower(),

            # provenance
            "source": chunk.metadata.get("source", "unknown"),
            "file": chunk.metadata.get("file", "unknown"),

            # structure awareness (if you added it earlier)
            "chapter": chunk.metadata.get("chapter", "unknown"),

            # optional but VERY useful
            "length": len(chunk.page_content)
        })
    
    return chunks
    
def build_splitter_recursive():
    """
    Build a RecursiveCharacterTextSplitter.
    
    chunk_size is measured in tokens by default (length_function=token_length).
    OR
    chunk_size is measured in characters by default (length_function=len).
    Based on config values, we can switch between the two. 
    """

    chunk_size=int(CHUNK_SIZE )
    chunk_overlap=int(CHUNK_OVERLAP) 
    length_function=get_length_function(LENGTH_FUNCTION)
    
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        is_separator_regex=False
    )    
    # separators=["\n\nChapter", "\nChapter", "\n\n", "\n", " ", ""]
    # is_separator_regex=True your separators are now treated as REGEX patterns, not plain text.
    # separators=["\n\n", "\n", ". ", " ", ""]

def get_length_function(LENGTH_FUNCTION):
    if LENGTH_FUNCTION == "token_length":
        return token_length
    elif LENGTH_FUNCTION == "character_length":
        return lambda x: len(x)
    elif LENGTH_FUNCTION == "len":
        return len
    else:
        raise ValueError(f"Invalid LENGTH_FUNCTION: {LENGTH_FUNCTION}")

def build_splitter_semantic(embeddings):
    """
    Build a SemanticSplitter.
    
    chunk_size is measured in tokens by default (length_function=token_length).
    OR
    chunk_size is measured in characters by default (length_function=len).
    Based on config values, we can switch between the two. 
    """

    return SemanticChunker(
        embeddings,
        breakpoint_threshold_type=BREAKPOINT_THRESHOLD_TYPE,
        breakpoint_threshold_amount=BREAKPOINT_THRESHOLD_AMOUNT,
        buffer_size=BUFFER_SIZE,
        min_chunk_size=MINIMUM_CHUNK_SIZE
    )
    
def split_by_chapter(docs):
    # chapter_pattern = r"(Chapter\s+\w+|CHAPTER\s+\w+)"
    chapter_pattern = r"(Chapter\s+[^\n]+|CHAPTER\s+[^\n]+)"
    new_docs = []

    for doc in docs:
        text = doc.page_content
        splits = re.split(chapter_pattern, text)

        current_chapter = "Unknown"

        for part in splits:
            if re.match(chapter_pattern, part):
                current_chapter = part.strip()
                continue

            if part.strip() and len(part.strip()) > 200:
                new_docs.append(
                    Document(
                        page_content=part,
                        metadata={
                            **doc.metadata,
                            "chapter": current_chapter
                        }
                    )
                )

    return new_docs