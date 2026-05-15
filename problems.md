🔴 1. Episode Boundary Problem
This is one of the hardest future problems.

Example:

robotic arm project
Later evolves into:

ROS debugging

embedded systems

AI vision integration

Questions:

same episode?

multiple subepisodes?

merged narratives?

Right now your architecture assumes:

correlation is obvious
but in reality:
episode segmentation is difficult.

🔴 2. Observation Linking Problem
You wrote:

“We connect relevant observations.”
But HOW?

This is actually a major research problem.

Eventually you’ll need:

embeddings

semantic similarity

temporal proximity

topic clustering

graph relationships

Otherwise:
episodes become inaccurate.

🔴 3. Episode TTL / Lifecycle Missing
You defined:

observation decay

SUM persistence

But episodic lifecycle is still vague.

Questions:

when does episode become inactive?

archived?

merged?

revived?

Example:

robotics project from 8 months ago
What happens if user resumes it?

This matters a lot.

🔴 4. Stable User Memory Is Slightly Underspecified
Right now SUM is:

stable semantic compression
Good.

But you still need:

categories.
Example:

{
  "interests": [],
  "preferences": [],
  "important_people": [],
  "active_goals": []
}
Otherwise:
SUM becomes vague over time.

🔴 5. Retrieval Architecture Is Missing
This is the BIGGEST missing component.

Right now you mainly defined:

memory formation.

But assistants become intelligent through:

context reconstruction.

Meaning:

Given current message,
what memory should be retrieved?
This is the real operational core.

Without retrieval:
memory is useless.

🔴 6. No Active Context Layer Yet
You currently have:

observations

episodes

SUM

But assistants usually also need:

Working Context
Meaning:

what is currently relevant RIGHT NOW?

Example:

currently active robotics project

current debugging issue

active conversation thread

This is closer to:

RAM
than long-term memory.

🧠 Suggested Missing Layer
You MAY eventually need:

Conversation
    ↓
Observations
    ↓
Episodes
    ↓
Working Context
    ↓
Stable User Memory
Where:

Working Context = active relevant state

VERY important later.

🔴 7. Promotion Policy Is Still Conceptual
You said:

frequency
duration
importance
reinforcement
Good.

But eventually you’ll need:

actual scoring formulas

thresholds

weighting systems

Example:

score =
(frequency * 0.3)
+
(recency * 0.2)
+
(duration * 0.2)
+
(emotional_weight * 0.1)
+
(user_confirmation * 0.2)
Not now.
But later.

🔴 8. Relationship Between SUM and Episodes
Potential future issue:

Suppose SUM says:

user interested in robotics
But for 2 years:

no robotics episodes appear.

Should SUM:

decay?

remain?

weaken?

This interaction still needs definition.