import gradio as gr

def hi(name):
    return f'Hi, {name}'

demo = gr.Interface(
    fn=hi,
    inputs="text",
    outputs="text",
    title="Gradio Simple Interface"
)


if __name__ == '__main__':
    demo.launch(share=True)