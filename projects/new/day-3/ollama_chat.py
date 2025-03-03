import gradio as gr

demo = gr.load_chat(
    "http://localhost:11434/",
    model="llama3.2:3b",
)

demo.launch()