import gradio as gr
from google import genai
from api_read import GEMINI_API_KEY

client = genai.Client(api_key= GEMINI_API_KEY)
 

def generate_res(input, modelName):
    return client.models.generate_content(
        model=modelName,
        contents=[input]
    ).text

# print(generate_res("hi"))

demo = gr.Interface(
    fn=generate_res,
    inputs=["text", gr.Dropdown(
            ["gemini-2.0-flash","gemini-2.0-flash-lite","gemini-1.5-pro"],
            label="select model",
            allow_custom_value=True
        )],
    outputs="text"
)

if __name__ == '__main__':
    demo.launch()