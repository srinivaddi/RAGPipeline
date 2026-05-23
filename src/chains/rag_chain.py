
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.prompts.rag_prompt import RAG_PROMPT_GROUNDED, RAG_PROMPT_ANALYSIS, RAG_PROMPT_CREATIVE
from src.config.settings import LOCAL_LLM_MODEL, RAG_PROMPT, TEMPERATURE

def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(retriever):
    llm = ChatOllama(
        model=LOCAL_LLM_MODEL,
        temperature=TEMPERATURE
    )
    def rag_chain(question: str):
        docs = retriever.invoke(question)
        context = _format_docs(docs)

        # messages = [
        #     SystemMessage(content=RAG_PROMPT_GROUNDED.format(context=context)),
        #     HumanMessage(content=question),
        # ]

        if RAG_PROMPT == "RAG_PROMPT_GROUNDED":
            messages = RAG_PROMPT_GROUNDED.format_messages(
                context=context,
                question=question,
            )
        elif RAG_PROMPT == "RAG_PROMPT_ANALYSIS":
            messages = RAG_PROMPT_ANALYSIS.format_messages(
                context=context,
                question=question,
            )
        elif RAG_PROMPT == "RAG_PROMPT_CREATIVE":
            messages = RAG_PROMPT_CREATIVE.format_messages(
                context=context,
                input=question,
            )
        
        response = llm.invoke(messages)

        # print(response.content)

        return {
            "result": response.content,
            "source_documents": docs,
        }

    return rag_chain
