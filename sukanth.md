HELLO 

00:49 14-06-26

Im going to create find_matching_observation function, it gets the new observation and compares it against all the existing episodes in the db and sees if anything matches. 

-> I wanted to use an LLM call or a neural network for it, but gpt recommend me to avoid using an llm cuz right, using an llm doesnt ensure determinism which is essential for memory. After a point the same epi and obse that was initially matched might not match cuz of a diff reasoing by the llm. 

soln: 

-> since its just phase 1 im going to stick to using a symbolic approach in matching the context of a observation and an episode. 

right now Ill use a symbolic system,

if topic matches -----> ill add a score of 0.5 to the total
if intent matches -----> ill add a score of 0.2 to the total
if entity matches -----> ill add a score of 0.3 to the total

if overall >0.7 add the obs to the current epi.

else create new episode.........

create new episode function is very trivial as of now, im just going to add the title, topic, intent, and the entity as it is from the observation as of now.

-----note to vijay-----: "bro as of now, I changed the the creation of the title from just taking the first topic in the observation to it joining all the topics and it is being done using a "/" to join all the topics in the obs. however in the future, when u are working with this again do ask me like making any changes to the """"create_episode"""" cuz my retrival logic works on that. 


-----note to suraj-----: suraj I restructured the architecture of the processor.py a bit and then I also added a id_counters.json file to the memory cuz it was missing. if u have any doubts in the cleaning of the processor.py, do let me know cuz earlier, the create_episode had a try and catch statement but then I deleted it and fixed the parameters for that funtion to make the code clean cuz the parameters of the functions arent going to change.



-----note to pawan------: I didnt modify any of ur code bro.

we have to chaneg the way in which we infer the title of the episode from the topics of the obs cuz just using a join is not going to cut it, but it is sufficient for phase one as of now. do let me know when u are working on this function".



future improvements: 

later on Ill change it to something that deals with sentence embeddings using,
BGE
E5
MiniLM
Nomic embeddings

then I can do a cosine similarity btwn the episode summary and the observation summary. 



future plan could be 

Phase 1
Keyword / symbolic matching

        ↓

Phase 2
Embedding similarity

        ↓

Phase 3
Hybrid retrieval
(Symbolic + Embedding + Episode metadata)

        ↓

Phase 4
LLM arbitration
(only for ambiguous matches)