from datetime import datetime
from .storage.db import generate_id

def create_observation(t, d):
    o = {
        "id": generate_id("obj"),
        "text": t,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topics": d.get("topics", []),
        "entities": d.get("entities", []),
        "intent": d.get("intent", ""),
        "metadata": {}
    }

    if not validate_observation(o):
        raise ValueError("Invalid observation")

    return o

def validate_observation(o):
    r = [
        "id",
        "text",
        "timestamp",
        "topics",
        "entities",
        "intent",
        "metadata"
    ]

    for k in r:
        if k not in o:
            return False

    if not isinstance(o["topics"], list):
        return False

    if not isinstance(o["entities"], list):
        return False

    if not isinstance(o["metadata"], dict):
        return False

    return True