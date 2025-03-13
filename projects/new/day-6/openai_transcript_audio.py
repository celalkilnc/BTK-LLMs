import requests
from openai import OpenAI
from api_read import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Fetch the audio file
url = "https://cdn.openai.com/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()

# Save the audio data to a temporary file
with open("temp_audio.wav", "wb") as audio_file:
    audio_file.write(response.content)

# Transcribe the audio using the correct API
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=open("temp_audio.wav", "rb"),
    language="tr"  # Türkçe transkript için
)

print("Transkript:", transcript.text)