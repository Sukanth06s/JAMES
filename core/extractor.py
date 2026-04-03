import json
from core.llm import call_llm


import json
from core.llm import call_llm

def extract_json(prompt):
    raw = call_llm(prompt)

    print("🔍 RAW LLM OUTPUT:\n", raw)  # Debug

    if not raw or not isinstance(raw, str):
        print("❌ Empty or invalid response")
        return {}

    cleaned = raw.strip()

    # -------------------------------
    # STEP 1: Remove markdown blocks
    # -------------------------------
    if "```" in cleaned:
        parts = cleaned.split("```")

        # Look for the block that contains JSON
        for part in parts:
            part = part.strip()

            if part.startswith("json"):
                part = part[4:].strip()  # remove 'json'
                cleaned = part
                break
            elif part.startswith("{"):
                cleaned = part
                break

    # -------------------------------
    # STEP 2: Extract JSON substring
    # -------------------------------
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end < start:
        print("❌ No valid JSON boundaries found")
        return {}

    json_str = cleaned[start:end + 1]

    # -------------------------------
    # STEP 3: Parse JSON safely
    # -------------------------------
    try:
        parsed = json.loads(json_str)
        return parsed

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        print("⚠️ Problematic JSON:\n", json_str)
        return {}

    except Exception as e:
        print("❌ Unexpected Error:", e)
        return {}

def extract_user_memory(user_input):
    prompt = f"""
You are a JSON extraction system.

Extract user-related information.
You are a JSON API.

You MUST return ONLY valid JSON.
Do NOT include:
- explanations
- markdown
- ```json
- any text outside JSON

If you fail, the system will crash.

Output must start with {{ and end with }}

STRICT RULES:
- Output MUST be valid JSON only
- Do NOT include any text outside JSON
- If nothing useful → return {{}}

Fields:
- name
- interests
- learning
- goals
- skills
- relationships (array of objects: name, role)

Input:
"{user_input}"

Format:
{{
  "name": "",
  "interests": [],
  "learning": [],
  "goals": [],
  "skills": [],
  "relationships": []
}}
"""
    return extract_json(prompt)


def extract_relation_memory(user_input):
    prompt = f"""
Extract how the user sees the AI.

STRICT JSON ONLY.

Fields:
- roles (role + priority 0–1)
- expectations
- interaction_style (tone, depth, challenge_level)

If nothing → return {{}}

Input:
"{user_input}"

Format:
{{
  "roles": [],
  "expectations": [],
  "interaction_style": {{}}
}}
"""
    return extract_json(prompt)