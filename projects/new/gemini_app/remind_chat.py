# Sohbeti hatırlasın
from google import genai
from api_read import GEMINI_API_KEY
import gradio as gr

client = genai.Client(api_key=GEMINI_API_KEY)

def chat_response(message, history):
    # Her yeni sohbet için chat oluştur
    chat = client.chats.create(model="gemini-pro")
    
    # Önceki konuşma geçmişini ekle
    for h in history:
        chat.send_message(h[0])  # Kullanıcı mesajı
    
    # Yeni mesajı gönder
    response = chat.send_message(message)
    return response.text

# Gradio arayüzü
demo = gr.ChatInterface(
    fn=chat_response,
    title="Gemini Sohbet Asistanı",
    description="Sohbet etmek için bir mesaj yazın. Sohbet geçmişiniz hatırlanacaktır.",
    examples=["Merhaba, nasılsın?", "Bana bir hikaye anlat"],
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()