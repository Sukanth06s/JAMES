def build_prompt(message):
    return f'''
    You are an information extraction engine.

    Task:
    Extract structured information from the user message.

    Output JSON only

    Schema:
    {{
        "topics": [],
        "entity": [],
        "intent": ""
    }}

    Definitions:
    Topics:
    - Main subjects or domains explicitly discussed.
    - Prefer broader concepts over specific details.
    - Do not infer topics not supported by the message.
    Entities:
    - Named people, organizations, technologies, tools, products, projects, places, courses, or other identifiable objects explicitly mentioned.
    Intent:
    - The primary activity explicitly being performed by the user.
    - Return a single intent.
    - If unclear, return an empty string.

    Rules:
    - Extract only explicitly mentioned information.
    - Do not infer personality.
    - Do not infer interests.
    - Do not infer emotions.
    - Do not infer goals.
    - Do not hallucinate.
    - Return valid Json only.
    - No markdown.
    - No explainations
    - No additional text.

    User message:
    {message}
    '''