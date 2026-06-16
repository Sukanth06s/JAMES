"""
The entry point.

what it does each loop iteration
    1. Read user input
    2. call processor.process_input()+memory pipeline runs
    3. print a basic response
    4. repeat untill user types 'exit'.

    it also calls ensure_memory_dir() once at startup so the 
    ./memory/ folder is generated to exist before anything else runs.
"""

from storage.db import ensure_memory_dir
from core.processor import process_input

def main():
    """
    interactive chat loop for JAMES
    """
    print("=" * 50)
    print("  James — Persistent Adaptive Assistant")
    print("  Type 'exit' to quit.")
    print("=" * 50)
 
    # ── One-time startup ──────────────────────────────────────────────────
    ensure_memory_dir()
    #create ./memory/folder if it doesn't exists
    #must happen  b4 any db.py function tries to write

     # ── Chat loop ─────────────────────────────────────────────────────────
    while True:
        user_input=input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower()=="exit":
            print("JAMES: Goodbye")
            break
     # ── Run the memory pipeline ───────────────────────────────────────
        result=process_input(user_input)
        obs=result["observation"]
        if obs is None:
            print("\nJames: Message received. No meaningful memory extracted.")
            continue
        # Display extracted observation signals
        intent    = obs.get("intent", "")
        topics    = obs.get("topics", [])
        obs_id    = obs["id"]
        print(f"\nJames: Got it. [{obs_id}] ")
        print(f"  Intent: {intent or 'unknown'} | Topics: {', '.join(topics) if topics else 'none detected'}")

        # display episode linking status
        episode=result.get("episode")
        status=result.get("status")

        if status =="matched" and episode:
            ep_id=episode.get("episode_id","N/A")
            ep_title=episode.get("title","untitled")
            ep_topics=episode.get("topics",[])
            print(f"  → Linked to existing episode [{ep_id}]: \"{ep_title}\"")
            if ep_topics:
                print(f"    Episode Topics: {', '.join(ep_topics)}")
        elif status == "created" and episode:
            ep_id = episode.get("episode_id", "N/A")
            ep_title = episode.get("title", "Untitled")
            ep_topics = episode.get("topics", [])
            print(f"  → Created new episode [{ep_id}]: \"{ep_title}\"")
            if ep_topics:
                print(f"    Episode Topics: {', '.join(ep_topics)}")
                
        elif status == "skipped":
            print("  → Episode linking skipped (non-memory-worthy message).")
        elif status == "no_episode_logic":
            print("  → Episode matching skipped (episode module not ready/fully integrated).")
        elif status == "no_create_episode":
            print("  → Episode matched None, but new episode creation is not ready.")
        elif status == "error":
            print("  → Episode matching error (failed during run).")
        else:
            print("  → Episode matching status: Pending / Not active.")

if __name__ == "__main__":
    main()