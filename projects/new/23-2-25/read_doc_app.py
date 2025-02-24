import google.generativeai as genai
import gradio as gr
import PyPDF2
import docx
import os

from api_read import GEMINI_API_KEY

# Google Gemini API yapılandırması
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# 📌 Belgeyi okuma fonksiyonları
def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        text += f"\n[Hata: PDF okunurken sorun oluştu: {str(e)}]\n"
    return text

def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        text = f"\n[Hata: DOCX okunurken sorun oluştu: {str(e)}]\n"
    return text

def read_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"\n[Hata: TXT dosyası okunurken sorun oluştu: {str(e)}]\n"

# 📌 Yüklenen dosyaların içeriğini al
def extract_text_from_files(files):
    document_text = ""
    for file in files:
        file_path = file.name
        lower_path = file_path.lower()
        if lower_path.endswith(".pdf"):
            document_text += read_pdf(file_path) + "\n"
        elif lower_path.endswith(".docx"):
            document_text += read_docx(file_path) + "\n"
        elif lower_path.endswith(".txt"):
            document_text += read_txt(file_path) + "\n"
        else:
            return "❌ Desteklenmeyen dosya türü."
    return document_text

# 📌 Sohbet işlevi
def chat_interface(user_input, file_inputs, chat_state):
    if chat_state is None:
        chat_state = {"history": [], "document_text": ""}
    
    # Yüklenen belgeler varsa içeriğini al ve sakla
    if file_inputs is not None and isinstance(file_inputs, list) and len(file_inputs) > 0:
        document_text = extract_text_from_files(file_inputs)
        chat_state["document_text"] = document_text
    else:
        document_text = chat_state.get("document_text", "")
    
    # Kullanıcı girişi boşsa, belge içeriğinin önizlemesini göster
    if not user_input.strip():
        preview = document_text[:1000] + ("..." if len(document_text) > 1000 else "")
        return "", [], f"📄 **Belge İçeriği:**\n\n{preview}", chat_state
    
    # Prompt oluşturma: Belge içeriği mevcutsa prompta ekle
    prompt = f"Belge içeriği:\n{document_text}\n\nUser: {user_input}\nAssistant:" if document_text else f"User: {user_input}\nAssistant:"
    
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"[Hata: Cevap oluşturulurken sorun oluştu: {str(e)}]"
    
    # Sohbet geçmişine ekleme (interleaved şekilde)
    chat_state["history"].append((user_input, reply))
    messages = []
    for u, a in chat_state["history"]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    
    curated_history = "\n\n".join([f"**User:** {u}\n**Assistant:** {a}" for u, a in chat_state["history"]])
    
    return "", messages, curated_history, chat_state

# 📌 Gradio Arayüzü
with gr.Blocks() as demo:
    gr.Markdown("## 📄 Çoklu Belge Destekli Chatbot")
    
    chat_state = gr.State()
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(label="Sohbet", type="messages")
            user_input = gr.Textbox(label="Sorunuzu Yazın")
            # "multiple" parametresi yerine "file_count" kullanılarak birden fazla dosya yüklenebilir.
            file_input = gr.File(
                label="Belgeleri Yükleyin (PDF, DOCX, TXT)",
                file_types=[".pdf", ".docx", ".txt"],
                interactive=True,
                file_count="multiple"
            )
            submit_btn = gr.Button("Gönder")
            clear_btn = gr.Button("Sohbeti Temizle")
        
        with gr.Column():
            raw_history = gr.Markdown("*Sohbet Geçmişi*")
    
    submit_btn.click(
        chat_interface,
        [user_input, file_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )
    
    user_input.submit(
        chat_interface,
        [user_input, file_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )
    
    # Sohbeti temizleyen fonksiyon
    def clear_chat():
        return "", [], "", {"history": [], "document_text": ""}
    
    clear_btn.click(
        clear_chat,
        None,
        [user_input, chatbot, raw_history, chat_state]
    )

demo.launch(show_error=True)
