import gradio as gr
from google import genai
from google.genai import types
import httpx
import os
from dotenv import load_dotenv
from api_read import GEMINI_API_KEY

# .env dosyasından API anahtarını yükle
load_dotenv()

# API anahtarını ayarla
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# API istemcisini oluştur
client = genai.Client(api_key=GEMINI_API_KEY)

# Sohbet geçmişini tutacak sözlük
chat_histories = {}

def process_chat(pdfs, pdf_url, message, history):
    try:
        session_id = str(pdfs) + str(pdf_url)  # PDF'lerin birleşiminden benzersiz ID oluştur
        current_history = chat_histories.get(session_id, [])
        
        pdf_contents = []
        
        # Yüklenen PDF dosyalarını işle
        if pdfs:
            for pdf in pdfs:
                # Dosya içeriğini doğrudan al
                if isinstance(pdf, dict) and 'data' in pdf:  # Yeni yüklenen dosya
                    pdf_data = pdf['data']
                else:  # Bytes olarak gelen dosya
                    pdf_data = pdf
                    
                pdf_contents.append(types.Part.from_bytes(
                    data=pdf_data,
                    mime_type='application/pdf'
                ))
        
        # URL'den PDF'i işle
        if pdf_url and pdf_url.strip():
            try:
                doc_data = httpx.get(pdf_url, timeout=60.0).content
                pdf_contents.append(types.Part.from_bytes(
                    data=doc_data,
                    mime_type='application/pdf'
                ))
            except Exception as e:
                error_message = f"PDF URL'si işlenirken hata: {str(e)}"
                history.append((message, error_message))
                return "", history
        
        if pdf_contents:  # PDF'ler varsa
            # Tüm PDF'ler ve mesajla birlikte API'yi çağır
            contents = [*pdf_contents, message]
            response = client.models.generate_content(
                model="gemini-1.5-pro",
                contents=contents
            )
        else:  # PDF yoksa normal sohbet
            response = client.models.generate_content(
                model="gemini-1.5-pro",
                contents=[
                    *[f"User: {h[0]}\nAssistant: {h[1]}" for h in current_history],
                    message
                ]
            )
        
        # Yanıtı al ve geçmişi güncelle
        bot_message = response.text
        current_history.append((message, bot_message))
        chat_histories[session_id] = current_history
        history.append((message, bot_message))
        return "", history

    except Exception as e:
        error_message = f"Bir hata oluştu: {str(e)}"
        history.append((message, error_message))
        return "", history

# Gradio arayüzünü oluştur
with gr.Blocks() as demo:
    gr.Markdown("# Çoklu PDF Sohbet ve Soru-Cevap Aracı")
    gr.Markdown("PDF dosyalarını yükleyin veya URL girin, belgeler hakkında sorular sorun.")
    
    with gr.Row():
        with gr.Column(scale=2):
            pdf_files = gr.File(
                label="PDF Dosyaları",
                file_types=[".pdf"],
                file_count="multiple",
                type="binary"
            )
        with gr.Column(scale=2):
            pdf_url = gr.Textbox(
                label="PDF URL'si (opsiyonel)", 
                placeholder="PDF dosyasının URL'sini girin...",
                show_label=True
            )
    
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, None),
    )
    
    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Mesajınızı yazın...",
            container=False
        )
        btn = gr.Button("Gönder", scale=1)
    
    clear = gr.Button("Sohbeti Temizle")
    
    # Örnek PDF ve sorular
    gr.Examples(
        examples=[
            [None, "https://dergipark.org.tr/en/download/article-file/228618", "Bu makaleyi Türkçe özetle"],
            [None, "", "Yapay zeka nedir ve nasıl çalışır?"],
        ],
        inputs=[pdf_files, pdf_url, txt],
    )
    
    # Event handlers
    btn.click(process_chat, [pdf_files, pdf_url, txt, chatbot], [txt, chatbot])
    txt.submit(process_chat, [pdf_files, pdf_url, txt, chatbot], [txt, chatbot])
    clear.click(lambda: ([], ""), outputs=[chatbot, txt])
    
    # PDF değişikliklerinde sohbeti temizle
    pdf_files.change(lambda: [], outputs=[chatbot])
    pdf_url.change(lambda: [], outputs=[chatbot])

if __name__ == "__main__":
    demo.launch()