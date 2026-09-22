from storage.db import append_observation
from core.candidate import process_observation


# ── Test observations ────────────────────────────────────

observation_1 = {
    "id": "test_obs_001",
    "text": "I am learning React and building an API",
    "timestamp": "2026-09-22 22:20:00",
    "topics": ["React", "API"],
    "entities": ["Node.js"],
    "intent": "learning",
    "metadata": {}
}

observation_2 = {
    "id": "test_obs_002",
    "text": "I am working on my React API project",
    "timestamp": "2026-09-22 22:21:00",
    "topics": ["React", "API"],
    "entities": ["Node.js"],
    "intent": "project",
    "metadata": {}
}

observation_3 = {
    "id": "test_obs_003",
    "text": "I am improving the React API and Node.js backend",
    "timestamp": "2026-09-22 22:22:00",
    "topics": ["React", "API"],
    "entities": ["Node.js"],
    "intent": "development",
    "metadata": {}
}


# ── Observation 1 ─────────────────────────────────────────

append_observation(observation_1)

result_1 = process_observation(observation_1)

print("\nObservation 1")
print("Status:", result_1["status"])
print("Candidate:", result_1["candidate"])


# ── Observation 2 ─────────────────────────────────────────

append_observation(observation_2)

result_2 = process_observation(observation_2)

print("\nObservation 2")
print("Status:", result_2["status"])
print("Candidate:", result_2["candidate"])


# ── Observation 3 ─────────────────────────────────────────

append_observation(observation_3)

result_3 = process_observation(observation_3)

print("\nObservation 3")
print("Status:", result_3["status"])
print("Candidate:", result_3["candidate"])
print("Episode:", result_3["episode"])