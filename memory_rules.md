***These are the rules and information that should be considered while extracting data from the user's prompt.***
1. Observation Schema:
    {
        "id": "",

        "text": "",

        "timestamp": "",

        "topics": [],

        "entities": [],

        "intent": "",

        "metadata": {}
    }

2. Topics:
    Definition:
    A topic represents the main subject/domain explicitly discussed in the message.

    Rules:
    Must be explicitly mentioned.
    Must not be inferred.
    Should be reusable across observations.
    Prefer broader concepts over tiny details.
    
    **Example**
    User:
    I'm debugging servo motors in my robotic arm.

    Good:
    ["robotics", "motor control"]
    
    Bad:
    ["servo motor model x100"]
    - because too specific

    Bad:
    ["engineering enthusiast"]
    - because it is an inference

3. Entity:
    Definition:
    Named people, projects, organizations, technologies, tools, products, places, etc.

    **Example**
    User:
    I'm working with Jason using Arduino.

    Good:
    [
        "Jason",
        "Arduino"
    ]

    Bad:
    [
        "friend"
    ]
    - Not explicitly mentioned.

4. Intent:
    Definition:
    Activity being performed.

    Examples:
    - learning
    - building
    - debugging
    - planning
    - researching
    - testing

    **Example**
    User:
    I'm learning React.

    Output:
    {
        "intent": "learning"
    }

    User:
    I'm debugging my robotic arm.

    Output:
    {
        "intent": "debugging"
    }

5. Store vs Ignore:
    **Store**
    Projects:
    - Building robotic arm

    Goals:
    - Learning React

    Collaborators:
    - Working with Jason

    Tools:
    - Using Arduino

    Preferences:
    - Prefer concise explanations

    **Ignore**
    Greetings:
    - Hello
    - Hi
    - Good morning

    Small acknowledgements:
    - Thanks
    - Cool
    - Nice

    Conversation filler:
    - Okay
    - Sure
    - Alright

# Future Plan
    Standalone observations (i.e., observations that don't belong to any episode) can be managed using a lifecycle system.
    If an observation isn't used for 30 days, it can be marked as inactive (archived but not deleted).
    If it remains inactive and its last access date crosses a configurable threshold (e.g., 100 days / 1 year), it can be permanently removed.
    Observations that belong to episodes should not be deleted automatically, since they are part of a larger context.