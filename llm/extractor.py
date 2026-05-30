import json
from ollama import chat
from .prompts import build_prompt

class Extractor:
    def __init__(self,model='qwen3:8b'):
        self.model=model
    def extract(self,message: str):
        prompt=build_prompt(message)
        response=chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        content=response["message"]["content"]
        return json.loads(content)