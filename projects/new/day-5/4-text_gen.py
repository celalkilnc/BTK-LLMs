from huggingface_hub import InferenceClient
from api_read import HF_API_KEY

client = InferenceClient(
	provider="hf-inference",
	api_key=HF_API_KEY
)

messages = [
	{
		"role": "user",
		"content": "Where is the capital of Turkey?"
	}
]

completion = client.chat.completions.create(
    model="CohereForAI/aya-23-8B", 
	messages=messages, 
	max_tokens=500,
)

print(completion.choices[0].message)