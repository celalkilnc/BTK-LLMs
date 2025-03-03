import gradio as gr
from google import genai
from api_read import GEMINI_API_KEY

client=genai.Client(api_key=GEMINI_API_KEY)

def process_audio(audio_file, prompt, model_sel, lang_sel):
    myfile = client.files.upload(file=audio_file)  # Upload the file
    prompt += " Translate the sound file in " + lang_sel+ " and also provide a transcript of the speech in time stamps"
    response = client.models.generate_content(
        model=model_sel,
        contents=[prompt, myfile]
    )
    return response.text

demo=gr.Interface(
  fn=process_audio,
  inputs=[gr.Audio(type="filepath"), #dosya yolu olarak yükleme yapılıyor, dosyanın kendisini göndermiyoruz
          gr.TextArea(label="prompt"), #kullanıcının promptunu yazacağı kısım
          gr.Dropdown(
              choices=["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash","gemini-1.5-pro"],
              value="gemini-2.0-flash"),
          gr.Dropdown(
            choices=["Turkish","English","Italian","German"],
            value="English"
          )],
  outputs=gr.TextArea(),
  title="Sound File Transcription Conversation"

)

if __name__=="__main__":
    demo.launch()