import { useEffect, useState } from "react";
import{
    getEpisodes,
    getEpisode,
    getEpisodeObservations
} from "../services/api"

function MemoryBrowser(){
    const[episodes,setEpisodes]=useState([]);
    const[selectedEpisode,setSelectedEpisode]=useState(null);
    const[observations,setObservations]=useState([]);
    const[loading,setLoading]=useState(true);
    const[error,setError]=useState("");
}

useState(()=>{
    loadEpisodes();
},[]);

async function loadEpisodes(){
    try{
        setLoading(true);
        setError("");

        const data=await getEpisodes();
        setEpisodes(data);
    } catch(err){
        console.error(err);
        setError(err.message);
    } finally{
        setLoading(false);
    }
}

async function selectedEpisode(episodeId)
{
    try{
        setError("");

        const [episode,episodeObservations]=
        await Promise.all([
            getEpisode(episodeId),
            getEpisodeObservations(episodeId),
        ]);
        setSelectedEpisode(episode);
        setObservations(episodeObservations);
    } catch(err){
        console.error(err);
        setError(err.message);
    }
}

if(loading){
    return(
        <section>
            <h2>Memory Browser</h2>
            <p>Loading memory...</p>
        </section>
    );
}

return(
    <section>
        <h2>Memory Browser</h2>
        {error && (
        <p>
          <strong>Error:</strong> {error}
        </p>
        )}
        <div>
            <h3>Episodes</h3>
            <button onClick={loadEpisodes}>Refresh</button>

            {episodes.length===0?(
                <p>No episodefound.</p>
            ):(
                <ul>
                    {episodes.map((episode)=>(
                        <li key={episode.episode_id}>
                            <button onClick={()=>
                                selectedEpisode(episode.episode_id)
                            }
                            >
                                {episode.title ||
                                 episode.episode_id}

                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>

        {selectedEpisode && (
        <div>
          <h3>Selected Episode</h3>

          <p>
            <strong>ID:</strong>{" "}
            {selectedEpisode.episode_id}
          </p>

          <p>
            <strong>Title:</strong>{" "}
            {selectedEpisode.title || "Untitled"}
          </p>

          <p>
            <strong>Topics:</strong>{" "}
            {selectedEpisode.topics?.join(", ") ||
              "None"}
          </p>

          <p>
            <strong>Participants:</strong>{" "}
            {selectedEpisode.participants?.join(", ") ||
              "None"}
          </p>

          <h4>Observations</h4>

          {observations.length === 0 ? (
            <p>No observations found.</p>
          ) : (
            <ul>
              {observations.map((observation) => (
                <li key={observation.id}>
                  {observation.text}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
)
export default MemoryBrowser;