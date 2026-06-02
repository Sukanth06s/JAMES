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