import gradio as gr
from google import genai
from api_read import GEMINI_API_KEY

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled , NoTranscriptFound, NoTranscriptAvailable


client=genai.Client(api_key=GEMINI_API_KEY)

url = "https://www.youtube.com/watch?v=E3szm_D5iEU&ab_channel=VEEDSTUDIO"

def get_transcript(url:str):
    video_id=url.split("v=")[1].split("&")[0]
    transcript=YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry["text"] for entry in transcript])


#print(get_transcript(url))

transcript=get_transcript(url)
prompt=f"Bu metni kısaca özetle: {transcript}"

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt]
    )

print(f"transcript: {transcript} \n ****************** \n summary: {response.text}")
