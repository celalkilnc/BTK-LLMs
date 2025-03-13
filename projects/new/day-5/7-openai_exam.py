from openai import OpenAI
from api_read import OPENAI_API_KEY

client = OpenAI(OPENAI_API_KEY)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
