"""
core/processor.py
-----------------

the most important file in the backend
this is pipeline orchestrator - it connect every module:

    User message
         ↓
    Extractor.extract()        [LLM Engineer's code]
         ↓
    _build_observation()       [your code — constructs the observation dict]
         ↓
    db.append_observation()    [your code — persists it]
         ↓
    [Episode matching — stub for Day 2, filled in Day 6 by Retrieval Eng]
         ↓
    returns response string
"""

import datetime                         #for timestamping observation
from llm.extractor import Extractor     
from storage.db import(
    generate_id,
    append_observation,
    load_all_episodes,
    append_episode,
    update_episode,
)
# ── Module-level extractor instance ──────────────────────────────────────────
# Created once so we don't reload the model on every message.
_extractor = Extractor()

# ── _build_observation ───────────────────────────────────────────────────────

def _build_observation(raw_text:str,extracted:dict)->dict:
    """
    combine the raw user text with LLM-extracted signals into a single structured
    observation dict that matches the schema

    args:
    raw_text:the original message user typed
    extracted:dict returned  by Extractor

    returns a complete observation dict ready to be stored
    """

    return{
        "id":generate_id("obj"),
        "text":raw_text,
        "entities":extracted.get("entities",[]),
        # named things mentioned: ppl, tools, project
        "topics":extracted.get("topics",[]),
        "intent":extracted.get("intent",""),
        # what user is doing:debugging,planning
        "importance":extracted.get("importance",0.0),
        #how significant it is
        "timestamp":datetime.datetime.utcnow().isoformat()+"2",
        "episode_id":None
        #will be filled when episode matching is done
    }

# ── _find_matching_episode  (STUB) ────────────────────────────────────────────
 
def _find_matching_episode(observation: dict):
    """
    stub
    this will inspect observation's topics/entities and return an existing episode dict if one is relevant
    for now it returns none
    """
    return None

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

    # ── Step 2: Build observation ─────────────────────────────────────────
    observation=_build_observation(user_message,extracted)
    #constructs the full observation dict with id, entities, timestamp,etc
    print("[processor] Built observation: {observation['id']}")

    # ── Step 3: Persist observation ───────────────────────────────────────
    append_observation(observation)
    #append to memory/observation.json atomically

    print(f"[processor] Saved observation {observation['id']} to disk")

     # ── Step 4: Episode matching  ────────────────────────────────────────
    matched_episode=_find_matching_episode(observation)

    if matched_episode:
        #update an existing episode with this observation
        matched_episode["related_observations"].append(observation["id"])
        update_episode(matched_episode)
        episode_result=matched_episode
    else:
        episode_result: None
    print(f"[processor] Episode: {'linked to' +str(episode_result) if episode_result else 'no match(stub)'}")

     # ── Step 5: Return summary ────────────────────────────────────────────
    return {
        "observation":observation,
        "episode":episode_result,
        "extracted":extracted,
    }
