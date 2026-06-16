# Day 1 (May 31, 2026):
    Created a rough observation schema (need to confirm) and some rules for proper extraction of data from the user's prompt - info is inside the file "memory_rules.md".

# Day 2 (June 1, 2026):
    Designed the code for creating an observation. Also defined some future plans that can be done to observation layer (refer memory_rules.md for more details).
    Code logic:
        As per the observation schema, the create_observation function creates and returns a dictionary with key-value pairs, some are passed as arguments while some are created inside function (eg datetime).
        There is also a function named validate_observation which is called inside the create_observation, as the name suggests it validates if the observation is in correct format.
        .get() function is used to store the values that are passed from the argument as this is makes sure the code doesn't crash if they are NULL, rather store with the default value that is mentioned in the second parameter of that function.
        .isinstance() function is used to check if the value (1st parameter) is in the required format (2nd parameter) (eg list, tuple, datatype)

# Day 3 (June 2, 2026):
    Fixed some bugs that were created by Suraj from last commit (with consent), held back some of those helper functions in "db.py" as it belongs to Backend Engineer and changed _build_observation() in processor.py to create_observation() as this calls the function that I created. _find_matching_episode() BELONGS TO RETRIEVAL ENGINEER, THIS FUNCTION SHOULD BE CALLED IN processor.py RATHER THAN DEFINING IN THE SAME FILE.

# Day 4 (June 11, 2026):
    Defined the schema for episodes and rules for creating/updating any episode, refer to memory_rules.md for more details. 
    Changed "entity" field name to "entities" in extraction-related files, as this is crucial.
    Added an important logic in processor.py to ignore non-observation worthy responses from user, as the previous code would still create an observation for them (like an empty json but only with an observation id). Because of which, main.py too undergone some changes with this logic and also fixed a small indent error.

# Day 5 (June 15, 2026):
    Fixed some small bugs in main.py and fixed a logic in processor.py, and also fixed the ".pyc" to "*.pyc" as only this will remove any .pyc files which are just useless for our project (used only by python hence which is irrelevant for us).
    And mainly removed the existing py cache files which are just irrelevant.

# Day 6 (June 16, 2026):
    Defined the code in schema.py file, this returns the pure schema of both the observation and episode layer, more like a helper function. Also deleted a print statement in main.py which is unnecessary.