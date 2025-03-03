import gradio as gr
from google import genai
from api_read import GEMINI_API_KEY
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled , NoTranscriptFound, NoTranscriptAvailable

#client=genai.Client(api_key=GEMINI_API_KEY)

def submit(url:str,lang:str,model_sel,word_count,gemini_api_key:str):
    client=genai.Client(api_key= gemini_api_key)
    video_id=url.split("v=")[1].split("&")[0]
    transcript=YouTubeTranscriptApi.get_transcript(video_id)

    prompt=f"Bu metni {lang} dilinde {word_count} sayıda kelime ile özetle: {transcript}"

    response = client.models.generate_content(
        model=model_sel,
        contents=[prompt]
    )
    
    return response.text,transcript

with gr.Blocks() as demo:
    with gr.Row():
            gemini_api_key = gr.Textbox(
                type="password",
                placeholder="Gemini API Key",
                label="Gemini API Key"
            )
            model_sel = gr.Dropdown(
              choices=["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash","gemini-1.5-pro"],
              value="gemini-2.0-flash",
              label="Model Selection"
            )
    with gr.Row():
        with gr.Column(scale=.3):
            url = gr.Textbox(
                placeholder="YouTube Video Url",
                label="YouTube Video Url"    
            )
            lang = gr.Dropdown(
                choices=["Turkish","English","Italian","German"],
                value="English",
                label="Output Language"
            )
            word_count = gr.Number(
                value=1000,
                step=10,
                label="Word Count"
            )
            btn_submit = gr.Button("Submit")
        with gr.Column():
            response = gr.TextArea(
                label="Ai Response"
            )
            transcript = gr.TextArea(
                label="Transcript"
            )

        btn_submit.click(
            fn=submit,
            inputs=[url,lang,model_sel,word_count,gemini_api_key],
            outputs=[response,transcript]
        )


if __name__=="__main__":
    demo.launch()