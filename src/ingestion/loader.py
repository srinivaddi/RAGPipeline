# loader.py
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader

def load_documents(
    input_path: str | os.PathLike,
) -> List[Document]:
    """
    Convenience wrapper for your project.
    Right now, it loads PDFs only.
    """
    # return load_pdfs(input_path)
    return load_pdfs(input_path, recursive=True)

# def load_pdfs(
#     path: str | os.PathLike,
#     recursive: bool = True,
#     silent_errors: bool = True,
# ) -> List[Document]:
#     """
#     Load PDFs from a file or directory into LangChain Document objects.

#     - If `path` is a PDF file: uses PyPDFLoader
#     - If `path` is a directory: uses PyPDFDirectoryLoader (loads all PDFs)

#     Returns: list[Document]
#     """
#     p = Path(path)

#     if not p.exists():
#         raise FileNotFoundError(f"Input path not found: {p.resolve()}")

#     if p.is_file():
#         if p.suffix.lower() != ".pdf":
#             raise ValueError(f"Expected a .pdf file, got: {p.name}")
#         loader = PyPDFLoader(str(p))
#         docs = loader.load()
#         return docs

#     # Directory case
#     # PyPDFDirectoryLoader loads all PDFs in the directory.
#     loader = PyPDFDirectoryLoader(
#         str(p),
#         recursive=recursive,
#         silent_errors=silent_errors,
#         glob="**/*.pdf",  # <- ensures nested PDFs are included
#     )
#     docs = loader.load()


#     if not docs:
#         # Helpful debug info: what PDFs exist?
#         pdfs = list(p.rglob("*.pdf")) if recursive else list(p.glob("*.pdf"))
#         raise RuntimeError(
#             f"No documents loaded. Found {len(pdfs)} PDF file(s) at {p.resolve()}.\n"
#             f"First few: {[str(x) for x in pdfs[:5]]}"
#         )

#     return docs

from pathlib import Path
import os
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

def load_pdfs(
    path: str | os.PathLike,
    recursive: bool = True,
    silent_errors: bool = True,
) -> List[Document]:
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"Input path not found: {p.resolve()}")

    # If it's a file, just load it
    if p.is_file():
        if p.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a .pdf file, got: {p.name}")
        return PyPDFLoader(str(p)).load()

    # If it's a directory, load all PDFs under it
    glob_pattern = "**/*.pdf" if recursive else "*.pdf"

    loader = DirectoryLoader(
        str(p),
        glob=glob_pattern,
        loader_cls=PyPDFLoader,
        silent_errors=silent_errors,
        show_progress=True,
        use_multithreading=True,
    )
    docs = loader.load()

    if not docs:
        pdfs = list(p.rglob("*.pdf")) if recursive else list(p.glob("*.pdf"))
        raise RuntimeError(
            f"No documents loaded. Found {len(pdfs)} PDF file(s) at {p.resolve()}.\n"
            f"First few: {[str(x) for x in pdfs[:5]]}"
        )

    return docs