from openai import OpenAI
from api_read import OPENAI_API_KEY
client=OpenAI(api_key=OPENAI_API_KEY)


audio_file = open(r"new\day-6\temp_audio.wav", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language="tr"
)
print(transcript)
