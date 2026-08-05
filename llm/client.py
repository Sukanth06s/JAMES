from groq import Groq
from dotenv import load_dotenv
from ollama import Client

import os

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ollama_client=Client(
    host="http://localhost:11434"
)