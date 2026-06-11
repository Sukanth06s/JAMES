"""
core/processor.py
-----------------

the most important file in the backend
this is pipeline orchestrator - it connect every module:

    User message
         ↓
    Extractor.extract()        [LLM Engineer's code]
         ↓
    create_observation()       [Memory Engineer's code — creates the observation dict]
         ↓
    db.append_observation()    [your code — persists it]
         ↓
    [Episode matching — stub for Day 2, filled in Day 6 by Retrieval Eng]
         ↓
    returns response string
"""

from .observation import create_observation
from .episode import (create_episode, add_observation_to_episode, find_matching_episode)
from llm.extractor import Extractor     
from storage.db import(
    append_observation,
    load_all_episodes,
    append_episode,
    update_episode,
)
# ── Module-level extractor instance ──────────────────────────────────────────
# Created once so we don't reload the model on every message.
_extractor = Extractor()

# ── process_input ─────────────────────────────────────────────────────────────

def process_input(user_message:str)->dict:
    """
    main pipeline entry point - called once per user message
    steps:
        1. extract structred signals from the message(LLM)
        2. build a complete observation object
        3. persist the observation to disk
        4. try to link observation to an existing episode (stub)
        5. return a summary dict that main.py can use
    """
    # ── Step 1: Extract ───────────────────────────────────────────────────
    print("[processor] Extracting signals from message.....")
    extracted=_extractor.extract(user_message)
    print(f"[processor] Extracted : {extracted}")

    # ── Step 2: Check if observation worthy and build if needed ─────────────────────────────────────────
    if (not extracted.get("topics") and not extracted.get("entities")) and extracted.get("intent")=="none":
        print("[processor] No meaningful memory extracted")
        return {
            "observation": None,
            "episode": None,
            "extracted": extracted
        }

    observation=create_observation(user_message,extracted)
    #constructs the full observation dict with id, entities, timestamp,etc
    print(f"[processor] Built observation: {observation['id']}")

    # ── Step 3: Persist observation ───────────────────────────────────────
    append_observation(observation)
    #append to memory/observation.json atomically

    print(f"[processor] Saved observation {observation['id']} to disk")

     # ── Step 4: Episode matching  ────────────────────────────────────────
    matched_episode=find_matching_episode(observation)

    if matched_episode:
        #update an existing episode with this observation
        matched_episode["related_observations"].append(observation["id"])
        update_episode(matched_episode)
        episode_result=matched_episode
    else:
        episode_result= None
    print(f"[processor] Episode: {'linked to' +str(episode_result) if episode_result else 'no match(stub)'}")

     # ── Step 5: Return summary ────────────────────────────────────────────
    return {
        "observation":observation,
        "episode":episode_result,
        "extracted":extracted,
    }
