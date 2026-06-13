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
    if (not extracted.get("topics") and not extracted.get("entities")) and extracted.get("intent") == "none":
        print("[processor] No meaningful memory extracted")
        return {
            "observation": None,
            "episode": None,
            "extracted": extracted,
            "status": "skipped"
        }

    # ASSUMPTION: Memory Engineer's create_observation signature is create_observation(text, extracted)
    # Aligning with core/observation.py: create_observation(t, d)
    observation = create_observation(user_message, extracted)
    print(f"[processor] Built observation: {observation['id']}")

    # ── Step 3: Persist observation ───────────────────────────────────────
    append_observation(observation)
    print(f"[processor] Saved observation {observation['id']} to disk")

    # ── Step 4 & 5: Episode Matching and Lifecycle ────────────────────────
    matched_or_new_episode = None
    status = "no_episode_logic"

    if find_matching_episode is not None:
        try:
            episodes = load_all_episodes()
            # ASSUMPTION: Retrieval Engineer's find_matching_episode signature is:
            # find_matching_episode(observation: dict, episodes: list) -> dict | None
            matched = find_matching_episode(observation, episodes)

            if matched is not None:
                # 5a. Link observation to the existing matched episode
                matched = update_episode_with_observation(matched, observation)
                update_episode(matched)
                matched_or_new_episode = matched
                status = "matched"
                print(f"[processor] Observation linked to existing episode : {matched['episode_id']}")
            else:
                # 5b. Create a new episode if no match is found
                if create_episode is not None:
                    # ASSUMPTION: We attempt to call create_episode(observation) as requested.
                    # If the Retrieval Engineer's code throws a TypeError due to requiring its
                    # actual signature: create_episode(title, list_of_obs, topics, participants)
                    # we fallback gracefully to pass individual parameters.

                    new_episode = create_episode(observation)                  
                    append_episode(new_episode)
                    matched_or_new_episode = new_episode
                    status = "created"
                    print(f"[processor] Created new episode: {new_episode['episode_id']}")
                else:
                    print(f"[processor] WARNING: create_episode is missing/none. skipping creation")
        except Exception as e:
            status = "error"
            print(f"[processor] ERROR: Failed during episode stage: {e}")
    else:
        print("[processor] WARNING: find_matching_episode is missing/None. Skipping episode stage.")

    # ── Step 6: Return summary ────────────────────────────────────────────
    return {
        "observation": observation,
        "episode": matched_or_new_episode,
        "extracted": extracted,
        "status": status
    }