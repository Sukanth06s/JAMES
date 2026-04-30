def build_personality(relation_memory):
    roles = relation_memory.get("roles", [])
    style = relation_memory.get("interaction_style", {})

    tone = "neutral"
    challenge = "medium"

    for r in roles:
        role = r.get("role")

        if role == "mentor":
            tone = "challenging"
        elif role == "friend":
            tone = "casual"

    if isinstance(style, dict) and "challenge_level" in style:
        challenge = style["challenge_level"]

    return {
        "tone": tone,
        "challenge": challenge
    }