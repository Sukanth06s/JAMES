import json
from .client import client
from .prompts import build_prompt

class Extractor:
    def __init__(self,model='google/gemma-4-26b-a4b-it:free'):
        self.model=model
    def extract(self,message: str):
        prompt=build_prompt(message)
        response=client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
        content=response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON")
            return {
                "topics": [],
                "entity": [],
                "intent": ""
            }