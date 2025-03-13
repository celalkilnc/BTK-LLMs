from huggingface_hub import InferenceClient
from api_read import GEMINI_API_KEY,HF_API_KEY

client = InferenceClient(
    provider="gf-inference",
    token = HF_API_KEY
)

response = client.zero_shot_classification(
    model="facebook/bart-large-mnli",
    text="this course is about LLMs knoowledge",
    candidate_labels=["refund","legal","faq"]
)

