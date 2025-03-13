from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")