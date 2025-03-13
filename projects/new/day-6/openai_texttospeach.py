import openai
from api_read import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="iyi dersler"
)
response.stream_to_file(r"openai_examples\speech.mp3")