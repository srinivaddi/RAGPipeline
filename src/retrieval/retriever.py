def build_retriever(vectorstore, k=8):
    return vectorstore.as_retriever(search_kwargs={"k": k})