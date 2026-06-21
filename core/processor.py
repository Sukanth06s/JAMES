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

from core.observation import create_observation
from llm.extractor import Extractor    
from core.episode import ( 
    update_episode_with_observation,
    find_matching_episode,
    create_episode
)
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

def process_input(user_message: str) -> dict:
    """
    main pipeline entry point - called once per user message
    steps:
        1. extract structured signals from the message (LLM)
        2. build a complete observation object
        3. persist the observation to disk
        4. try to link observation to an existing episode (stub)
        5. return a summary dict that main.py can use
    """
    # ── Step 1: Extract ───────────────────────────────────────────────────
    print("[processor] Extracting signals from message.....")
    extracted = _extractor.extract(user_message)
    print(f"[processor] Extracted : {extracted}")

    # ── Step 2: Check if observation worthy and build if needed ───────────
    if (not extracted.get("topics") and not extracted.get("entities")) and (extracted.get("intent") == "none" or extracted.get("intent") == ""):
        print("[processor] No meaningful memory extracted")
        return {
            "observation": None,
            "episode": None,
            "extracted": extracted,
            "status": "skipped"
        }

    # Build observation object
    observation = create_observation(user_message, extracted)
    print(f"[processor] Built observation: {observation['id']}")

    # ── Step 3: Persist observation ───────────────────────────────────────
    append_observation(observation)
    print(f"[processor] Saved observation {observation['id']} to disk")

    # ── Step 4 & 5: Episode Matching and Lifecycle ────────────────────────
    matched_or_new_episode = None
    status = "error"

    
    try:
        episodes = load_all_episodes()
        matched = find_matching_episode(observation, episodes)

        if matched is not None:
            # 5a. Link observation to the existing matched episode
            matched = update_episode_with_observation(matched, observation)
            update_episode(matched)
            matched_or_new_episode = matched
            status = "matched"
            print(f"[processor] Observation linked to existing episode : {matched['episode_id']}")
        else:
            # create a new episode if no match is found
            new_episode = create_episode(observation)                  
            append_episode(new_episode)
            matched_or_new_episode = new_episode
            status = "created"
            print(f"[processor] Created new episode: {new_episode['episode_id']}")
    except ValueError as ve:
            # Propagate schema validation failures so they are caught immediately during testing
            raise ve
    except Exception as e:
         status="error"
         print(f"\n[processor] !!! ERROR: failed during episode stage: {e}!!!\n")

    # ── Step 6: Return summary ────────────────────────────────────────────
    return {
        "observation": observation,
        "episode": matched_or_new_episode,
        "extracted": extracted,
        "status": status
    }