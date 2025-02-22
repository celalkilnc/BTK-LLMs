from google import genai
from google.genai import types
from api_read import GEMINI_API_KEY
import pathlib
import PIL.Image

image_path_1 = "bass.jpg"   
image_path_2 = "verstappen.jpg"  
image_path_3 = "f1.jpg" 
pil_image = PIL.Image.open(image_path_1)

b64_image = types.Part.from_bytes(
    data=pathlib.Path(image_path_2).read_bytes(),
    mime_type="image/jpg"
)
pil_image3 = PIL.Image.open(image_path_3)

#downloaded_image = requests.get(image_url_1)

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents=["Resimlerdeki ortak noktaları ve farklılıkları söyle",
              pil_image, b64_image, pil_image3])

print(response.text)