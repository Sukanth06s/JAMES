"""
config.py
-------
Central place for every settings the rest of the system needs.
By keeping paths and the models here, you only ever change
one file when moving to a different  machine or upgrading the model
"""

# config.py
 
# ── LLM ──────────────────────────────────────────────────
MODEL_NAME="qwen3:8b"
# This must match the model string used in extractor.py
# model is defaulted here
# change here ->change everywhere

# ── Memory file paths ────────────────────────────────────
MEMORY_PATH ="./memory/"
# Root folder that holds all json memory files
OBSERVATIONS_FILE="./memory/observations.json"
# every raw observations from user input is appended here
# format : json array [{...},{...}]
EPISODES_FILE="./memory/episodes.json" 
# grouped structured context built from observations
#format : json array 
USER_PROFILE_FILE="./memory/user_profile.json"
# long term stable user facts
#format: json object {...}

# ── ID counters file ─────────────────────────────────────
ID_COUNTERS_FILE="./memory/id_counters.json"
# tracks the last numeric suffix of obj_xx and epi_xx ids
#format : {"obj":0, "epi":0}