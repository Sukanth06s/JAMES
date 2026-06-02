"""
storage/db.py
-------------
every read and write to disk goes through this file
no other modules  should open files directly - they always call these functions.
(swap json for sql lite later)

functions exported:
    load_json(path,default)    -> load file or return default
    save_json(path,data)       -> overwrite a file safely
    append_json(path,item)     -> add one item to json array file
    generate_id(prefix)        -> "obj_001", "epi_002" , etc
    ensure_memory_dir()        -> create ./memory/ if missing
"""

import json       #reading and writing json
import os         #checking whether files / directories exists
from config import(
    MEMORY_PATH, OBSERVATIONS_FILE, EPISODES_FILE, USER_PROFILE_FILE, ID_COUNTERS_FILE,
)

# ── ensure_memory_dir ────────────────────────────────────────────────────────

def ensure_memory_dir():
    """
    create ./memory/ folder if it does not exists
    called once at start in main.py so every other function can assume the folder is there
    """
    os.makedirs(MEMORY_PATH,exist_ok=True)
    # exist_ok=True means: don't crash if the folder already exists.
 
 
# ── load_json ────────────────────────────────────────────────────────────────
 
def load_json(path:str,default):
    """
    safely loads a json file from disk

    args:
    path    : file path to load
    default : value to return whn file is missing or empty
              (pass [] for array and {} for object)

    it returns parsed Python object (list or dict)

    y 'default' coz on 1st run no memory files exist . so instead of crashing we return default so as to rest of code can run normally
    """
    
    if not os.path.exists(path):
        #file doesn't exists
        return default
    try:
        with open(path,"r",encoding="utf-8") as f:
            content=f.read().strip()
        if not content:
            # file exists but empty 
            return default
        
        return json.loads(content)
    except json.JSONDecodeError:
        # file is corrupted
        print(f"[db] WARNING: could not parse {path} - using default.")
        return default

# ── save_json ────────────────────────────────────────────────────────────────
 
def save_json(path:str,data):
    """
    overwrite a json file with new data

    the write  is done a temp file 1st then renamed
    this is called as atomic write-
    if process crashes halfway through, the original file doesn't get corrupted

    args:
        path : destination file path
        data : any JSON-serialisable Python object (list or dict) 
    """

    tmp_path = path+".tmp"
    #step 1 write everything down to a temp file
    with open(tmp_path,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
        # indent=4    → human-readable formatting (easier to debug)
        # ensure_ascii=False → keeps non-ASCII characters (e.g. names)

    #step 2- atomically rename to real
    os.replace(tmp_path,path)
    # os.replace is atomic on both Linux and Windows.
 
 
# ── append_json ──────────────────────────────────────────────────────────────

def append_json(path:str,item:dict):
     """
    Add a single dict to a JSON array file.
 
    If the file does not exist yet, it is created with [item] as
    its sole contents.
 
    Args:
        path : path to a JSON file whose top-level value is an array
        item : the dict to append
    """
     existing=load_json(path,default=[])
     #load what's already there
     existing.append(item)
     #add the new item in the end of the list
     save_json(path,existing)
     #write the updated list in disk

# ── User profile helpers ─────────────────────────────────────────────────────
 
def load_user_profile()->dict:
     """
    Load the stable user memory object.
    Returns a dict with empty defaults if the file doesn't exist yet.
    """
     default_profile={
         "name":"",
         "interests":[],
         "goals":[],
         "preferences":[],
         "important_people":[],
     }
     return load_json(USER_PROFILE_FILE,default=default_profile)

def save_user_profile(profile:dict):
    """
    Persist the user profile dict back to disk.
    """
    save_json(USER_PROFILE_FILE, profile)

# ── ID generator ─────────────────────────────────────────────────────────────
 
def generate_id(prefix:str)->str:
    """
    return next sequential id for a given prefix
    IDs are stored in memory/id_counters.json so they survive restarts
    """
    counters=load_json(ID_COUNTERS_FILE,default={})
    #load existing counters (or empty dict on 1st run)
    current=counters.get(prefix,0)
    new_count=current+1
    counters[prefix]=new_count
    #update count in memory
    save_json(ID_COUNTERS_FILE,counters)
    #persist the update counter to disk 
    return f"{prefix}_{str(new_count).zfill(3)}"
    #zfill(3) ->pads to 3 digits: 1->"001" 12->"012" 100->"100"

# ── Observation helpers ───────────────────────────────────────────────────────
 
def append_observation(observation:dict):
    """
    saves one observation in observation file
    called by processor.py after building an observation object
    """
    append_json(OBSERVATIONS_FILE,observation)

def load_all_observations()->list:
    """
    return every observation stored
    """
    return load_json(OBSERVATIONS_FILE,default=[])

# ── Episode helpers ───────────────────────────────────────────────────────────
 
def append_episode(episode:dict):
    """
    save a brand new episode to episode file
    """
    append_json(EPISODES_FILE,episode)

def load_all_episodes()->list:
    """
    return every episode
    """
    return load_json(EPISODES_FILE,default=[])

def update_episode(updated_episode:dict):
    """
    replace an existing episode with updated version
    args:
    updated_episode: the full episode dict with changes
    """
    episodes=load_all_episodes()
    # find the index of episode to replace
    for i,ep in enumerate(episodes):
        if ep.get("episode_id")==updated_episode.get("episode_id"):
            episodes[i]=updated_episode
            #swap old episode out , new one in
            save_json(EPISODES_FILE,episodes)
            return 
    #fallback: episode_id not found thenjust append
    print(f"[db]WARNING: episode {updated_episode.get('episode_id')} not found - appending instead")
    episodes.append(updated_episode)
    save_json(EPISODES_FILE,episodes)
    