from config import MODEL_FILE, USER_FILE, RELATION_FILE
from core.memory_manager import load_json, save_json
from core.extractor import extract_user_memory, extract_relation_memory
from core.personality import build_personality
from core.llm import call_llm
from utils.helpers import merge_list, merge_relationships


# ---------------- DEFAULT STRUCTURES ----------------

MODEL_DEFAULT = {
    "model": {
        "name": "James",
        "role": "Personal AI assistant",
        "capabilities": ["text conversation"],
        "limitations": [],
        "ethics": [],
        "restrictions": [],
        "future_capabilities": []
    }
}

USER_DEFAULT = {
    "user": {
        "name": "",
        "interests": [],
        "learning": [],
        "goals": [],
        "skills": [],
        "relationships": []
    }
}

RELATION_DEFAULT = {
    "roles": [],
    "expectations": [],
    "interaction_style": {}
}


# ---------------- LOAD MEMORY ----------------

model_memory = load_json(MODEL_FILE, MODEL_DEFAULT)
user_memory = load_json(USER_FILE, USER_DEFAULT)
relation_memory = load_json(RELATION_FILE, RELATION_DEFAULT)


# ---------------- MERGE FUNCTIONS ----------------

def update_user_memory(new_data):
    if not isinstance(new_data, dict):
        return

    user = user_memory.setdefault("user", {})

    # Ensure structure exists
    user.setdefault("name", "")
    user.setdefault("interests", [])
    user.setdefault("learning", [])
    user.setdefault("goals", [])
    user.setdefault("skills", [])
    user.setdefault("relationships", [])

    # ✅ FIXED name handling (before assignment)
    name = new_data.get("name", "").strip()
    if name and name.lower() not in ["james", "assistant", "ai"]:
        user["name"] = name

    # Lists
    for key in ["interests", "learning", "goals", "skills"]:
        if key in new_data and isinstance(new_data[key], list):
            merge_list(user[key], new_data[key])

    # Relationships
    if "relationships" in new_data and isinstance(new_data["relationships"], list):
        merge_relationships(user["relationships"], new_data["relationships"])

    save_json(USER_FILE, user_memory)


def update_relation_memory(new_data):
    global relation_memory

    if not isinstance(new_data, dict):
        return

    # 🔥 Normalize if nested
    if "relationship" in new_data:
        new_data = new_data["relationship"]

    # Ensure structure exists
    relation_memory.setdefault("roles", [])
    relation_memory.setdefault("expectations", [])
    relation_memory.setdefault("interaction_style", {})

    if "roles" in new_data and isinstance(new_data["roles"], list):
        merge_list(relation_memory["roles"], new_data["roles"])

    if "expectations" in new_data and isinstance(new_data["expectations"], list):
        merge_list(relation_memory["expectations"], new_data["expectations"])

    if "interaction_style" in new_data and isinstance(new_data["interaction_style"], dict):
        relation_memory["interaction_style"].update(new_data["interaction_style"])

    save_json(RELATION_FILE, relation_memory)


# ---------------- MAIN AI FUNCTION ----------------

def james(query):
    print("🧠 USER MEMORY:", user_memory)
    print("🤝 RELATION:", relation_memory)

    personality = build_personality(relation_memory)

    prompt = f"""
You are James.

Personality:
Tone: {personality['tone']}
Challenge Level: {personality['challenge']}

User:
{user_memory}

Respond naturally.

User: {query}
"""

    response = call_llm(prompt)

    # Extract memory safely
    user_data = extract_user_memory(query) or {}
    relation_data = extract_relation_memory(query) or {}

    update_user_memory(user_data)
    update_relation_memory(relation_data)

    return response


# ---------------- RUN LOOP ----------------

if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        reply = james(user_input)
        print("James:", reply)