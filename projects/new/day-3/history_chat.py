# 

import gradio as gr
import google.generativeai as genai
from api_read import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def generative_res(message,history):
  chat_history=[]
  for message_pair in history:

    if isinstance(message_pair,(list,tuple)) and len(message_pair)==2: # len(message_pair)==2 => user and system
      human,ai=message_pair
      chat_history.extend( # extend listeye liste ekler
        [
          {"role":"user","parts": [human]},
          {"role":"model","parts":[ai]}
        ]
      ) 

  chat=model.start_chat(history=chat_history)

  response=chat.send_message(message)
  return response.text


demo = gr.ChatInterface(
   fn=generative_res,
   title="chat bot",
   examples=[
      "kimim ben",
      "burası ne"
   ],
   theme='soft'
)

if __name__ == '__main__':
    demo.launch()