Indexing (offline)  ingestion/, embeddings/, vectorstore/
Retrieval (online)  retrieval/
Generation          prompts/, chains/
Serving             api/


ingestion/
    loaders.py → PDF, web, text loaders
    splitters.py → chunk size / overlap
    ingest.py → glue code that builds the index

data/
    raw/ – PDFs, markdown, text files
    processed/ – pre‑chunked or cleaned text (optional but useful)

For a standard LangChain RAG pipeline (load → chunk → embed → retrieve → generate):
Required

langchain – core framework [pypi.org]
langchain-community – document loaders + vector stores [pypi.org]
langchain-openai – embeddings + chat models (can be swapped) [docs.langchain.com]
langchain-ollama – embeddings + chat models (can be swapped) [docs.langchain.com]
langchain-text-splitters – chunking utilities [stackoverflow.com]
python-dotenv – load env vars from .env
pydantic – config and data models (LangChain dependency)


uv pip install \
  langchain \
  langchain-community \
  langchain-openai \
  langchain_ollama \
  langchain-text-splitters \
  faiss-cpu \
  python-dotenv


uv pip install \
  langchain \
  langchain-community \
  langchain_ollama \
  langchain-text-splitters \
  chromadb \
  python-dotenv


project has two completely different flows:
  Phase 1 Indexing (offline)    Runs before user query    Create a searchable knowledge base
  Phase 2 Query / RAG (online)  Runs Per user request     Retrieve + generate answer

PHASE 1: INDEXING FLOW (offline)
  Turn raw documents into a vector store retriever
  Step 1 – Raw data (data/raw/)  
    These are never sent directly to the LLM.
  Step 2 – Document loading 
    src/ingestion/loaders.py
      input        
        loader = TextLoader("text.txt")
        documents = loader.load()
      output
        [
          Document(page_content="...", metadata={...}),
          ...
        ]
  Step 3 – Chunking
    src/ingestion/splitters.py
      splitter = RecursiveCharacterTextSplitter(
          chunk_size=1000,
          chunk_overlap=200,
      )
      chunks = splitter.split_documents(documents)
    Models retrieve chunks, not full documents
    Improves recall
    Prevents context overflow
  Step 4 – Embedding
    src/embeddings/embedder.py
      embeddings = OpenAIEmbeddings()
      vectors = embeddings.embed_documents(chunks)
    Each chunk → numerical vector
  Step 5 – Vector store creation
    src/vectorstore/store.py
      vectorstore = FAISS.from_documents(chunks, embeddings)
      vectorstore.save_local("vectorstore/")
    A persisted semantic index
    No LLM involved yet
  Step 5 – Retriever creation
    Later (during runtime)
      retriever = vectorstore.as_retriever(k=4)
    That’s the only object the RAG pipeline needs from indexing

PHASE 2: QUERY / RAG FLOW (online)
  Happens every time a user asks a question
  Step 1 – User query arrives
    From Gradio/FastAPI/CLI
      question = "What is this project about
  Step 2 – Retriever fetches relevant chunks
    src/retrieval/retriever.py
      input
        docs = retriever.invoke(question)
      output
        [
          Document(page_content="relevant chunk 1", ...),
          Document(page_content="relevant chunk 2", ...),
        ]
  Step 3 – Context formatting
    src/chains/rag_chain.py
      context = "\n\n".join(doc.page_content for doc in docs)
      "Chunk 1 text...
      Chunk 2 text..."
  Step 4 – Prompt assembly
    src/prompts/rag_prompt.py
      Use the given context to answer the question.
      If you don't know the answer, say you don't know.
        Context:
        {context}
      system_prompt = RAG_PROMPT.format(context=context)
  Step 5 – Message construction (chat‑model compliant)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question),
    ]
    This is where retrieval meets generation 
  Step 6 – LLM invocation
    rag_chain.py
      response = llm.invoke(message
    output
      AIMessage(content="Answer grounded in retrieved context
  Step 7 – Final structured return
    return {
        "result": response.content,
        "source_documents": docs,
    }

Full runtime flow summary (single glance)
  User Question
    ↓
  Retriever (vector search)
    ↓
  Relevant Document Chunks
    ↓
  Context Formatter
    ↓
  RAG Prompt
    ↓
  LLM (ChatOpenAI)
    ↓
  Answer + Sources


StepCode                        responsibility
--------------------------------------------------------
User submits question           api/app.py
rag_chain() invoked             src/chains/rag_chain.py
retriever.invoke()              src/retrieval/retriever.py
Vector search                   src/vectorstore/store.py
Prompt formatting               src/prompts/rag_prompt.py
LLM calllang                    chain_openai.ChatOpenAI
Response returned               api/app.py → UI
 