from openai import OpenAI
from api_read import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.moderations.create(
    input = "I want to kill my black slave"
)

score_dict = vars(response.results[0].category_scores)
highest_category = max([(k, v) for k, v in score_dict.items() if v is not None], key=lambda x: x[1])

print(response)
print(f"Highest category: {highest_category[0]} ({highest_category[1]:.4f})")
print(f"Flagged: {response.results[0].flagged}")