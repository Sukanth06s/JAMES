def empty_observation():
    return {
        "id": "",
        "text": "",
        "timestamp": "",
        "topics": [],
        "entities": [],
        "intent": "",
        "metadata": {}
    }

def empty_episode():
    return {
        "episode_id": "",
        "title": "",
        "status": "",
        "topics": [],
        "participants": [],
        "related_observations": [],
        "created_at": "",
        "last_updated": "",
        "metadata": {}
    }