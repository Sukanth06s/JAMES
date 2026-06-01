# 1ST JUNE 2026
**config.py**
Every hardcoded path is a future bug. If the memory folder moves or the
model changes, you'd have to hunt through every file. I centralized all
settings here so there's one place to change anything, and every other
module just imports from config.

**storage/db.py**
This is the most important thing I built today. The principle I followed
was: no other module should ever open a file directly. Everything goes
through db.py. The reason is isolation — if we move from JSON to SQLite
in Phase 2, only this file changes, not processor.py or main.py.

The two specific decisions I thought hard about:

*Atomic writes* — I write to a `.tmp` file first, then rename it to the
real file. A normal `open(..., "w")` leaves a window where a crash
mid-write corrupts the file. With rename, either the old version survives
or the new one is complete — never a half-written state. Memory corruption
was one of the risks we discussed in the architecture, so I wanted to
eliminate it at the storage level.

*generate_id()* — IDs are stored in `id_counters.json` so they survive
restarts. Without persistence, every restart resets to `obs_001` and you
get ID collisions across sessions. The counters file is the simplest
solution that actually works long-term.

**core/processor.py**
The pipeline needed to be complete enough to run end-to-end today, but
not block on work that isn't done yet (Retrieval Engineer's episode
matching is Day 6). So I wired extraction → observation → storage fully,
and made `_find_matching_episode()` a stub that returns `None`. This way
the pipeline runs without crashing, and the Retrieval Engineer just fills
in that one function — nothing else changes.

**main.py**
Kept it minimal on purpose. The response today is just a printout of the
obs ID and extracted topics — a placeholder. The real LLM response gets
wired in Day 9. The important thing is `ensure_memory_dir()` runs before
anything else, so no file operation ever fails because the folder doesn't
exist.