from storage.db import(
    load_all_candidates,load_all_observations,append_candidate,update_candidate,delete_candidate,append_episode,generate_id
)
from core.episode import(
    create_episode,update_episode_with_observation
)
from core.utils import get_current_time
from storage.db import generate_id

# ── Candidate settings ───────────────────────────────────
TOPIC_WEIGHT=0.4
# a weight given to topic similarity
ENTITY_WEIGHT=0.6
# a weight given to entity similarity
SIMILARITY_THRESHOLD=0.60
#a minimum score required for an observation
# to match an existing candidate

MIN_OBSERVATIONS_FOR_EPISODE=3
# minimum no of related observations required
# before candidate is promoted to a episode

# ── Similarity helpers ───────────────────────────────────

def normalise(values):
    #converts values into lowercase strings
    # and removes duplicate values
    return set(str(value).lower() for value in values)

def calculate_jaccard(first,second):
    #calculates jaccard similarity between two sets
    # J(A,B)=|A ∩ B|
    #        -------
    #        |A U B|    
    first=normalise(first)
    second=normalise(second)

    union=first.union(second)

    #if both sets are empty, there is no information
    # to compare, so similarity is zero
    if not union:
        return 0.0
    intersection=first.intersection(second)
    return len(intersection)/len(union)

def calculate_topic_jaccard(observation,candidate):
    #compare observation topics with candidate topics
    observation_topics=observation.get("topics",[])
    candidate_topics=candidate.get("topics",[])

    return calculate_jaccard(observation_topics,candidate_topics)

def calculate_entity_jaccard(observation, candidate):
    # compares observation entities with candidate participants
    observation_entities = observation.get("entities", [])
    candidate_entities = candidate.get("participants", [])

    return calculate_jaccard(
        observation_entities,
        candidate_entities)

def calculate_score(observation,candidate):
    #candidate the final candidate similarity score
    topic_score=calculate_topic_jaccard(observation,candidate)
    entity_score=calculate_entity_jaccard(observation,candidate)
    return (
        TOPIC_WEIGHT*topic_score+ENTITY_WEIGHT*entity_score
    )

# ── Candidate creation ───────────────────────────────────

def create_candidate(observation):
    candidate={
        "candidate_id":generate_id("cand"),
        "title":"/".join(observation.get("topics",[])) or "General Context",
        "status":"candidate",
        "topics":observation.get("topics",[]).copy(),
        "participants":observation.get("entities",[]),
        "related_observations":[observation["id"]],
        "created_at":get_current_time(),
        "last_updated":get_current_time()
    }
    append_candidate(candidate)
    return candidate

# ── Candidate update ─────────────────────────────────────
def update_candidate_with_observation(candidate,observation):
    for topic in observation.get("topics",[]):
        if topic not in candidate["topics"]:
            candidate["topics"].append(topic)

    for entity in observation.get("entities", []):
        if entity not in candidate["participants"]:
            candidate["participants"].append(entity)

    candidate["related_observations"].append(observation["id"])
    candidate["last_updated"]=get_current_time()
    update_candidate(candidate)
    return candidate

# ── Candidate matching ───────────────────────────────────
def find_matching_candidate(observation,candidates):
    #finds highest similarality score
    best_candidate=None
    best_score=0.0

    for candidate in candidates:
        score=calculate_score(observation,candidate)
        if score> best_score:
            best_score=score
            best_candidate=candidate

    #candidate is accepted only when its source
    # reaches configured similarity threshold 
    if best_candidate is not None and best_score>=SIMILARITY_THRESHOLD:
        return best_candidate

# ── Candidate promotion ──────────────────────────────────

def promote_candidate(candidate):
    observations=load_all_observations()
    observation_ids=set(candidate.get("related_observations",[]))
    #retrieves the actual observations belonging to this candidate

    candidate_observations=[
        observation
        for observation in observations
        if observation.get("id") in observation_ids
        ]
    # safety check
    if not candidate_observations:
        return None
    #use the first observation to create the episode
    episode=create_episode(candidate_observations[0])
    #add the remaining observations to the episode
    for observation in candidate_observations[1:]:
        episode = update_episode_with_observation(
            episode,
            observation
        )
    append_episode(episode)

    delete_candidate(candidate["candidate_id"])
    return episode

# ── Candidate processing ─────────────────────────────────

def process_observation(observation):
    candidates=load_all_candidates()
    #check whether observation matches any existing candidate
    matching_candidate=find_matching_candidate(observation,candidates)

    #no existing candidate matched
    #so create a new candidate
    if matching_candidate is None:
        candidate=create_candidate(observation)
        return{
            "status":"candidate",
            "candidate":candidate,
            "episode":None
        }

    #matching candidate found
    candidate=update_candidate_with_observation(matching_candidate,observation)

    #once has required no of observations then promote
    if len(candidate["related_observations"])>=MIN_OBSERVATIONS_FOR_EPISODE:
        episode=promote_candidate(candidate)
        return {
             "status": "promoted",
            "candidate": None,
            "episode": episode
        }
    # candidate has not reached the promotion threshold yet
    return {
        "status": "candidate",
        "candidate": candidate,
        "episode": None
    }