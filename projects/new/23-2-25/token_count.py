from api_read import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)


myFile = client.files.get(name="lx1vypih3sfr")
response = client.models.count_tokens(
  model='gemini-2.0-flash',
  contents=[myFile]
)

print(response) 
