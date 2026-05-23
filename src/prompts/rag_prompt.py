from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT_GROUNDED = ChatPromptTemplate.from_template(
    # Respond as is
    """
    Answer the question using only the provided context.
    If you don't know the answer, say you don't know.

    Context:
    {context}

    Question:
    {question}
    """
)

RAG_PROMPT_ANALYSIS = ChatPromptTemplate.from_template(
    # Respond Analysis
    """
    You are an expert literary analyst.
    Using the provided context, analyze the content.
    
    Context:
    {context}

    Question:
    {question}
    """
)

RAG_PROMPT_CREATIVE = ChatPromptTemplate.from_template(
    # Respond Creative
    """
    You are an creative literary analyst.
    Use the provided context as inspiration, but you may also use your general knowledge and imagination to expand on the ideas.

    Context:
    {context}

    Question:
    {input}

    Instructions:
    - Provide a rich, thoughtful, and engaging answer
    - You may infer, interpret, and elaborate beyond the exact text
    - Make the answer vivid and insightful, not just factual
    """
)


