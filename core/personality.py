def build_personality(relation_memory):
    roles = relation_memory.get("roles", [])
    style = relation_memory.get("interaction_style", {})

    tone = "neutral"
    challenge = "medium"

    for r in roles:
        if r.get("role") == "mentor":
            tone = "challenging"
        elif r.get("role") == "friend":
            tone = "casual"

    if "challenge_level" in style:
        challenge = style["challenge_level"]

    return {
        "tone": tone,
        "challenge": challenge
    }