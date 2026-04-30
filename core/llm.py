import ollama
from config import MODEL_NAME


def call_llm(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={"num_gpu": 0}
    )

    return response["message"]["content"]