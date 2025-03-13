from openai import OpenAI
from PIL import Image
import requests
from api_read import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.images.generate(
    model="dall-e-3",
    prompt="scooby-doo and shaggy and the monster of the swamp",
    n=1,
    size="1024x1024"
)

image_url = response.data[0].url

image_res = Image.open(requests.get(image_url, stream=True).raw)

image_res.show()
