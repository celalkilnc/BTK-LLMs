import gradio as gr
from google import genai
from smolagents import DuckDuckGoSearchTool
from api_read import GEMINI_API_KEY

search_tool = DuckDuckGoSearchTool()
client=genai.Client(api_key=GEMINI_API_KEY)

def search_answer(question:str) -> str: # -> return type belirler
    """ Func Information """
    result = search_tool(question)
    prompt = f'''
    Verilen soruyu arama sonuçlarına göre cevapla.
    Soru:{question}
    Sonuç:{result}
    Verdiğin bilgilerin arama sonucuna dayalı olmasına dikkat et.
    '''
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt]
    )
    return response.text

#print(search_answer("2024 F1 şampiyonu kimdir?"))

demo = gr.Interface(
    fn=search_answer,
    inputs = [gr.Textbox()],
    outputs=[gr.TextArea()]
)

if __name__=="__main__":
    demo.launch()