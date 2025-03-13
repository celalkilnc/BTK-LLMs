import gradio as gr
from openai import OpenAI
from api_read import OPENAI_API_KEY , LAWYER_ID,TEACHER_ID, SPORT_TRINER_ID, COACH_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def process_instruction(instruction, model_key):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=instruction
    )
    
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=getModelId(model_key)
    )
    
    messages = client.beta.threads.messages.list(thread.id)
    for msg in reversed(list(messages)):
        if msg.role == "assistant":
            return msg.content[0].text.value.strip()
    return "Sorry, I cannot help at the moment."

interface = gr.Interface(
    theme="Professional Theme",
    fn=process_instruction,
    inputs=[
        gr.Textbox(label="Enter your instruction"),
        gr.Dropdown(choices=["Sports Coach", "Chemistry Teacher", "Thracian Trainer"], label="Select Model")
    ],
    outputs=gr.Textbox(label="Assistant Response"),
    title="Local OpenAI Assistant",
    description="Local Gradio interface working with the same assistant ID"
)

def getModelId(model_key:str) -> str:
    model_ids = {
        "Sports Coach": COACH_ID,
        "Chemistry Teacher": TEACHER_ID,
        "Thracian Trainer": SPORT_TRINER_ID,
    }
    
    return model_ids.get(model_key, "Invalid model key")

if __name__ == "__main__":
    interface.launch()