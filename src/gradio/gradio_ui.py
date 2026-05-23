import gradio as gr
from src.api.app import query, initialize
import webbrowser
import threading
import time

def open_gradio(chat): 
    threading.Thread(target=open_browser).start()
    gr.ChatInterface(
        fn=chat,
        # type="messages",
        title="LOTR RAG Chat ⚔️",
        description="Ask anything about Middle-earth"
    ).queue().launch()

def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:7860")
    
def add_inline_refs(answer, docs):
    refs = " ".join([f"[{i}]" for i in range(1, min(len(docs), 4)+1)])
    return f"{answer}\n\n{refs}"

