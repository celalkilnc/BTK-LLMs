import requests
from api_read import GEMINI_API_KEY, HF_API_KEY 

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
header = {"Authorization": "Bearer " + HF_API_KEY}

def query(payload):
    return requests.post( API_URL, headers = header, json = payload).json()

output = query({
    "inputs": "Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!",
    "parameters":{
        "candidate_labels":["refund","legal","faq"]
    }
})

print(output['labels'][0],output['scores'][0])
