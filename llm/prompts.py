def build_prompt(message):
    return f'''
    You are an information extraction engine

    Task:
    Extract structured information from the user message

    Output JSON only

    Schema:
    {{
        "entities": [],
        "topics": [],
        "intent": "",
        "importance": 0.0,
    }}

    Rules:
    - Extract only explicitly mentioned information.
    - Do not infer personality.
    - Do not infer interests.
    - Do not infer emotions.
    - Do not hallucinate.
    - Return valid Json only.

    User message:
    {message}
    '''