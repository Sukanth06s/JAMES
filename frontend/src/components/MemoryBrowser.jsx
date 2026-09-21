import { useEffect, useState } from "react";
import {
    getEpisode, // Changed from getEpisodes to match your api.js export
    getEpisodeById,
    getEpisodeObservations
} from "../services/api";

function MemoryBrowser() {
    // 1. State Declarations
    const [episodes, setEpisodes] = useState([]);
    const [selectedEpisode, setSelectedEpisodeState] = useState(null);
    const [observations, setObservations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // 2. Lifecycle hook (Triggers loadEpisodes on mount)
    useEffect(() => {
        loadEpisodes();
    }, []);

    // 3. Helper function to load all episodes
    async function loadEpisodes() {
        try {
            setLoading(true);
            setError("");
            
            // Calls getItem singular to match your api.js definition
            const data = await getEpisode(); 
            setEpisodes(data);
        } catch (err) {
            console.error(err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    // 4. Handles item clicks and fetches deep metrics simultaneously
    async function handleEpisodeClick(episodeId) {
        try {
            setError("");
            const [episode, episodeObservations] = await Promise.all([
                getEpisodeById(episodeId),
                getEpisodeObservations(episodeId),
            ]);
            setSelectedEpisodeState(episode);
            setObservations(episodeObservations);
        } catch (err) {
            console.error(err);
            setError(err.message);
        }
    }

    // 5. Component Render Guard Conditions
    if (loading) {
        return (
            <section>
                <h2>Memory Browser</h2>
                <p>Loading memory...</p>
            </section>
        );
    }

    // 6. Main UI Return JSX
    return (
        <section>
            <h2>Memory Browser</h2>
            {error && (
                <p style={{ color: "red" }}>
                    <strong>Error:</strong> {error}
                </p>
            )}
            <div>
                <h3>Episodes</h3>
                <button onClick={loadEpisodes}>Refresh</button>

                {episodes.length === 0 ? (
                    <p>No episodes found.</p>
                ) : (
                    <ul>
                        {episodes.map((episode) => (
                            <li key={episode.episode_id}>
                                <button onClick={() => handleEpisodeClick(episode.episode_id)}>
                                    {episode.title || episode.episode_id}
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {selectedEpisode && (
                <div>
                    <h3>Selected Episode</h3>
                    <p><strong>ID:</strong> {selectedEpisode.episode_id}</p>
                    <p><strong>Title:</strong> {selectedEpisode.title || "Untitled"}</p>
                    <p><strong>Topics:</strong> {selectedEpisode.topics?.join(", ") || "None"}</p>
                    <p><strong>Participants:</strong> {selectedEpisode.participants?.join(", ") || "None"}</p>

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
    );
}

export default MemoryBrowser;
