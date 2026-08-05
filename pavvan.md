Day 1
- Made basic extraction structure
- haven't decided proper schema yet, will discuss with vijay and finalise it.
- haven't decided proper model yet. just using qwen-38b for now gpt suggested it
- extraction is a bit slow. needs to be optimised
- created __init__.py in tests,llm and root for path related issues


03.06.2026
llm/clients.py
- this file is created cause i changed it from local llm to openrouter. using gemma 4 for now (might change it later)
- imported OpenAI cause it can also call gemma4 
- imported load_dotenv to load api key from .env
- client is exported to other files to call the llm
- it is done so that it is not required to call the api key in every file

llm/prompts.py
- updated the extraction schema - contains { topics:[], entity: [], intent: "" }

llm/extractor.py
- imported client to call llm from client.py and build_prompt to build prompt from prompts.py
- in extract function we get the final prompt for extraction by inserting user message to the extraction prompt
- client calls the llm and the result is stored in response. The proper response is stored in content
- try catch statement is used to avoid some errors

for testing it is run by the command: python -m tests.test_pipeline
might get error 429. it means overload to the model.


05.08.2026
client.py
- added ollama client for presentation purpose if we dont get internet there (but ollama is slower than groq)
extractor.py
- introduced USE_GROQ(hardcoded gateway). if USE_GROQ=1, groq client is used or else ollama client is used
- recieved the response of both llms in the same variable content