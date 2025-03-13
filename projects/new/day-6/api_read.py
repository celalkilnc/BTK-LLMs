from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEACHER_ID = os.getenv("TEACHER_ID")
LAWYER_ID = os.getenv("LAWYER_ID")
SPORT_TRINER_ID = os.getenv("SPORT_TRINER_ID")
COACH_ID = os.getenv("COACH_ID")