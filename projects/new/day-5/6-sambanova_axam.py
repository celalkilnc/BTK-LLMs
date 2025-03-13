from api_read import SAMBANOVA_API_KEY
import os
import openai
client = openai.OpenAI(
    api_key=SAMBANOVA_API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="DeepSeek-R1-Distill-Llama-70B",
    messages=[{"role":"system",
    "content":"You are a helpful assistant"},
    {"role":"user","content":"3.9 mu büyük 3.11 mi"}],
    temperature=0.1,
    top_p=0.1
)

print(response.choices[0].message.content)