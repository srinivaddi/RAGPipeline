from src.api.app import query, initialize
from src.gradio.gradio_ui import open_gradio

def chat(message, history):
    answer, docs = query(message)
    # answer = add_inline_refs(answer, docs)
    partial = ""
    for char in answer:
        partial += char
        yield partial


# start app
if __name__ == "__main__":
    initialize()  # ✅ run ONCE
    open_gradio(chat)