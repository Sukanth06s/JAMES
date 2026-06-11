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
    print("  (Day 2 build — memory pipeline active)")
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
        intent    = obs.get("intent", "")
        topics    = obs.get("topics", [])
        obs_id    = obs["id"]
        print(f"\nJames: Got it. [{obs_id}] "
            f"Intent: {intent or 'unknown'} | "
            f"Topics: {', '.join(topics) if topics else 'none detected'}")
    
    # ── Entry point guard ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
    # Only runs when you execute `python main.py` directly.
    # Does NOT run when another module imports main.py.
 
 