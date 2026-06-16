from storage.db import generate_id
from core.observation import validate_observation
from core.utils import get_current_time


def create_episode(observation: dict) -> dict:
    """
    Create a new episode from a single observation.

    Called when no existing episode matches.
    """
    title = " / ".join(observation.get("topics", []))
    if not title:
        title = "General Context"
    episode = {
        "episode_id": generate_id("ep"),
        "title": title,
        "status": "active",
        "topics": observation.get("topics", []).copy(),
        "participants": observation.get("entities", []).copy(),
        "related_observations": [
            observation["id"]
        ],
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

def update_episode_with_observation(
    episode: dict,
    observation: dict
) -> dict:
    
    if not validate_episode(episode):
        raise ValueError("Invalid episode")
    if not validate_observation(observation):
        raise ValueError("Invalid observation")

    for i in observation["topics"]:
        if i not in episode["topics"]:
            episode["topics"].append(i)
            
    for p in observation["entities"]:
        if p not in episode["participants"]:
            episode["participants"].append(p)
    
    episode["related_observations"].append(observation["id"])
    episode["last_updated"] = get_current_time()
    return episode

def find_matching_episode(
    observation: dict,
    episodes: list
) -> dict | None:
    """
    Return best matching episode.
    Returns:
        episode dict
        OR
        None
    """

    best_episode = None
    best_score = 0

    obs_topics = set(
        t.lower()
        for t in observation.get("topics", [])
    )

    obs_entities = set(
        e.lower()
        for e in observation.get("entities", [])
    )

    for episode in episodes:

        score = 0

        ep_topics = set(
            t.lower()
            for t in episode.get("topics", [])
        )

        ep_participants = set(
            p.lower()
            for p in episode.get("participants", [])
        )

        # Topic overlap
        topic_overlap = len(
            obs_topics.intersection(ep_topics)
        )

        score += topic_overlap * 3

        # Participant overlap
        participant_overlap = len(
            obs_entities.intersection(ep_participants)
        )

        score += participant_overlap * 2

        if score > best_score:
            best_score = score
            best_episode = episode

    MATCH_THRESHOLD = 3

    if best_score >= MATCH_THRESHOLD:
        return best_episode

    return None