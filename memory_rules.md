# These are the rules and information that should be considered while extracting data from the user's prompt.
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

# These are the rules and information that should be considered for creating a new episode or updating an existing episode.
1. Episode Schema:
    {
        "episode_id": "",

        "title": "",
        
        "status": "",
        
        "topics": [],
        
        "participants": [],
        
        "related_observations": [],
        
        "created_at": "",
        
        "last_updated": "",
        
        "metadata": {}
    }

2. Title:
    This is a small string which gives a note about what a particular episode is used for.

3. Status:
    This just says if the episode is active (used recently), inactive (used a long time ago), or closed.

4. **When to create/update:**
    - Updation:
        This is the first step. When a new observation is created, it should check with already existing episodes, if they tend to match, then this observation is also linked to that existing episode.
    - Creation:
        When the above process fails, i.e, if the observation doesn't match with any existing episodes, then the next step, it should check with previously existing observations, if atleast any 2 observations (or more) match, a new episode will be created with respect to these observations.
    - If all the above steps fail, then they just exist as a standalone observation.
 
# Future Plan
    Standalone observations (i.e., observations that don't belong to any episode) can be managed using a lifecycle system.
    If an observation isn't used for 30 days, it can be marked as inactive (archived but not deleted).
    If it remains inactive and its last access date crosses a configurable threshold (e.g., 100 days / 1 year), it can be permanently removed.
    Observations that belong to episodes should not be deleted automatically, since they are part of a larger context.