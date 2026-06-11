from datetime import datetime
from .storage.db import generate_id
from .observation import validate_observation

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_episode(title, list_of_obs, topics, participants):
    episode = {
        "episode_id": generate_id("epi"),
        "title": title,
        "status": "active",
        "topics": topics,
        "participants": participants,
        "related_observations": list_of_obs,
        "created_at": get_current_time(),
        "last_updated": get_current_time(),
        "metadata": {}
    }
    if not validate_episode(episode):
        raise ValueError("Invalid episode")

    return episode

def validate_episode(episode):
    fields = ["episode_id", "title", "status", "topics", "participants", "related_observations", "created_at", "last_updated", "metadata"]
    for f in fields:
        if f not in episode:
            return False
    if not isinstance(episode["related_observations"], list):
        return False
    if not isinstance(episode["metadata"], dict):
        return False
    if not isinstance(episode["topics"], list):
        return False
    if not isinstance(episode["participants"], list):
        return False
    return True

def add_observation_to_episode(epis, obs):
    if not validate_episode(epis):
        raise ValueError("Invalid episode")
    if not validate_observation(obs):
        raise ValueError("Invalid observation")

    for i in obs["topics"]:
        if i not in epis["topics"]:
            epis["topics"].append(i)
    epis["related_observations"].append(obs["id"])
    epis["last_updated"] = get_current_time()
    return epis

def find_matching_episode():