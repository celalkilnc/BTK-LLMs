from openai import OpenAI
from api_read import OPENAI_API_KEY

client=OpenAI(api_key=OPENAI_API_KEY)

result=client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            "role":"user",
            "content":[
                {
                    "type":"text", 
                    "text":"briefly describe the picture"
                },
                {
                    "type":"image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                        }
                }
            ],
        }
    ],
)

print (result + "\n\n\n\n\n*******************\n\n\n\n\n")
print(result.choices[0].message.content)