import gradio as gr

def hi_plus(name,count):
    return f"{name} \n" * count

#print(hi_plus("test",5))

demo = gr.Interface(
    fn=hi_plus,
    inputs=[
        gr.Text(label = "Your Name"),
        gr.Slider(minimum = 1, maximum = 10)
    ],
    outputs=gr.Textbox(max_lines=10),
    title = "Say my name"
)


if __name__ == '__main__':
    demo.launch()