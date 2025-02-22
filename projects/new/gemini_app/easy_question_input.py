from google import genai
from api_read import GEMINI_API_KEY
import gradio as gr

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(question):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question,
    )
    return response.text

iface = gr.Interface(
    fn=generate_response,
    inputs="text",
    outputs="text",
    title="Gemini Question Generator",
    description="Enter a question to get a response from the Gemini model."
)

iface.launch()