#This is just a test file to check for groq models
from llm.client import groq_client

models=groq_client.models.list()

for model in models.data:
    print(model.id)