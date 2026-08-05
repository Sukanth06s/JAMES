import json
from .client import groq_client,ollama_client
from .prompts import build_prompt
from groq import RateLimitError
from groq import APIError

USE_GROQ=0

class Extractor:
    def __init__(self,groq_model='llama-3.3-70b-versatile',ollama_model="qwen3:8b"):
        self.groq_model=groq_model
        self.ollama_model=ollama_model
    def extract(self,message: str):
        prompt=build_prompt(message)
        if USE_GROQ==1:
            response=groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
            content=response.choices[0].message.content
        else:
            response=ollama_client.chat(
                model=self.ollama_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            content=response["message"]["content"]
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()
        try:
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