import json
from .client import client
from .prompts import build_prompt
from groq import RateLimitError
from groq import APIError

class Extractor:
    def __init__(self,model='llama-3.3-70b-versatile'):
        self.model=model
    def extract(self,message: str):
        prompt=build_prompt(message)
        try:
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
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()
            return json.loads(content)
        except json.JSONDecodeError:
            print("Invalid JSON")
            return {
                "topics": [],
                "entities": [],
                "intent": ""
            }
        except RateLimitError:
            print("Groq Rate limit reached.")
            return{
                "topics": [],
                "entities": [],
                "intent": ""
            }
        except APIError as e:
            print(e)
            return{
                "topics": [],
                "entities": [],
                "intent": ""
            }