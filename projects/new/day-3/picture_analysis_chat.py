from google import genai
import gradio as gr
from api_read import GEMINI_API_KEY

# API anahtarınızla client'ı başlatın
client = genai.Client(api_key = GEMINI_API_KEY)

def chat_interface(user_input,model_sel, image_input, chat_state):
    # Eğer chat_state mevcut değilse, sohbet geçmişini içeren bir sözlük başlatın.
    if chat_state is None:
        chat_state = {"history": []}
    
    # Boş mesaj durumunda, mevcut geçmişi uygun formatta döndürün.
    if not user_input.strip():
        # chat_state["history"] şu anda tuple listesi; bunları sözlük listesine dönüştürüyoruz.
        messages = []
        for u, a in chat_state["history"]:
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content": a})
        curated_history = "\n\n".join([f"*user: {u}\n\nassistant*: {a}" for u, a in chat_state["history"]])
        return "", messages, curated_history, chat_state

    # Sohbet geçmişini prompt olarak derleyelim.
    prompt = ""
    for u, a in chat_state["history"]:
        prompt += f"User: {u}\nAssistant: {a}\n"
    prompt += f"User: {user_input}\nAssistant: "

    # Resim varsa, hem resmi hem prompt'u gönderiyoruz.
    if image_input:
        response = client.models.generate_content(
            model=model_sel,
            contents=[image_input, prompt]
        )
    else:
        response = client.models.generate_content(
            model=model_sel,
            contents=[prompt]
        )

    reply = response.text  # Asistanın cevabı

    # Yeni etkileşimi geçmişe ekleyin.
    chat_state["history"].append((user_input, reply))

    # Gradio Chatbot bileşeni için geçmişi "messages" formatına dönüştürün.
    messages = []
    for u, a in chat_state["history"]:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})
    
    # Ekstra, düzenlenmiş geçmişin metin hali.
    curated_history_lines = []
    for u, a in chat_state["history"]:
        curated_history_lines.append(f"*user*: {u}")
        curated_history_lines.append(f"*assistant*: {a}")
    curated_history = "\n\n".join(curated_history_lines)

    return "", messages, curated_history, chat_state

# Gradio arayüzü
with gr.Blocks(theme = gr.themes.Ocean().set(
     body_background_fill="#FFFFFF"
), css_paths= "projects/new/day-3/gr_style_test.css") as demo:
    gr.Markdown("## Gemini 2.0 Flash Chat")
    
    # Sohbet geçmişini saklamak için state.
    chat_state = gr.State()
    
    with gr.Row():
        with gr.Column():
            # type parametresini "messages" olarak ayarlıyoruz.
            chatbot = gr.Chatbot(label="Conversation", type="messages")
            user_input = gr.Textbox(label="Your Message")
            model_sel = gr.Dropdown(
                choices=["gemini-2.0-flash","gemini-2.0-flash-lite","gemini-1.5-pro"],
                value="gemini-2.0-flash"
            )
            submit_btn = gr.Button("Gönder")
            attach_button = gr.Button("📷 Resim Ekle", scale=1)
            image_input = gr.Image(
                type="pil",
                label="Resim Yükle",
                visible=False,
                scale=1
            )
        with gr.Column(scale=0.3):
            raw_history = gr.Markdown("*Conversation History*")
    
    # Resim ekleme butonuna tıklanınca resim yükleme alanını görünür yapalım.
    def toggle_image_upload():
        return gr.update(visible=True)
    
    attach_button.click(
        toggle_image_upload,
        [],
        [image_input]
    )
    
    # "Gönder" butonuna veya Enter tuşuna basıldığında chat_interface çalışsın.
    submit_btn.click(
        chat_interface,
        [user_input,model_sel, image_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )
    
    user_input.submit(
        chat_interface,
        [user_input,model_sel, image_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )


demo.launch(show_error=True)