import { useEffect, useState } from "react";
import {
    getEpisode, // Changed from getEpisodes to match your api.js export
    getEpisodeById,getCandidates,
    getEpisodeObservations
} from "../services/api";

function MemoryBrowser() {
    // 1. State Declarations
    const [episodes, setEpisodes] = useState([]);
    const [candidates, setCandidates] = useState([]);
    const [selectedEpisode, setSelectedEpisodeState] = useState(null);
    const [observations, setObservations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // 2. Lifecycle hook (Triggers loadEpisodes on mount)
    useEffect(() => {
        loadEpisodes();
        loadCandidates();
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

    async function loadCandidates() {
        try {
            setError("");

            const data = await getCandidates();
            setCandidates(data);
        } catch (err) {
            console.error(err);
            setError(err.message);
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

    return (
    <section className="memory-view">

        <div className="page-header">
            <div>
                <span className="section-label">
                    LONG-TERM MEMORY
                </span>

                <h2>Memory & History</h2>

                <p>
                    Browse episodes and observations stored by
                    JAMES across previous interactions.
                </p>
            </div>

            <div className="view-indicator">
                <span className="indicator-dot"></span>
                {episodes.length}{" "}
                {episodes.length === 1 ? "Episode" : "Episodes"}
            </div>
        </div>


        {/* ERROR */}
        {error && (
            <div className="memory-error">
                <strong>Memory service error:</strong>
                <span>{error}</span>
            </div>
        )}


        <div className="memory-layout">

            {/* =================================================
                LEFT — EPISODE HISTORY
               ================================================= */}

            <div className="memory-list-card">

                <div className="memory-list-header">

                    <div>
                        <span className="card-label">
                            STORED EPISODES
                        </span>

                        <h3>
                            Episode History
                        </h3>
                    </div>

                    <button
                        className="refresh-button"
                        onClick={loadEpisodes}
                    >
                        Refresh
                    </button>

                </div>


                {episodes.length === 0 ? (

                    <div className="memory-empty">

                        <div className="empty-symbol">
                            M
                        </div>

                        <strong>
                            No episodes found
                        </strong>

                        <p>
                            JAMES has not stored any episodes yet.
                        </p>

                    </div>

                ) : (

                    <div className="episode-list">

                        {episodes.map((episode) => (

                            <button
                                key={episode.episode_id}
                                className={`episode-list-item ${
                                    selectedEpisode?.episode_id ===
                                    episode.episode_id
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleEpisodeClick(
                                        episode.episode_id
                                    )
                                }
                            >

                                <div className="episode-list-content">

                                    <span className="episode-list-title">
                                        {episode.title ||
                                            "Untitled Episode"}
                                    </span>

                                    <span className="episode-list-id">
                                        {episode.episode_id}
                                    </span>

                                </div>

                                <span className="episode-arrow">
                                    →
                                </span>

                            </button>

                        ))}

                    </div>

                )}

            </div>
                        


            {/* =================================================
                CANDIDATE MEMORY
               ================================================= */}

            <div className="memory-list-card">

                <div className="memory-list-header">

                    <div>
                        <span className="card-label">
                            ACTIVE CANDIDATES
                        </span>

                        <h3>
                            Candidate Memory
                        </h3>
                    </div>

                    <button
                        className="refresh-button"
                        onClick={loadCandidates}
                    >
                        Refresh
                    </button>

                </div>

                {candidates.length === 0 ? (

                    <div className="memory-empty">

                        <div className="empty-symbol">
                            C
                        </div>

                        <strong>
                            No candidates found
                        </strong>

                        <p>
                            No provisional memories are currently active.
                        </p>

                    </div>

                ) : (

                    <div className="episode-list">

                        {candidates.map((candidate) => (
                            <div
                            className="episode-list-item"
                            key={candidate.candidate_id}
                        >

                            <div className="episode-list-content">

                                <span className="episode-list-title">
                                    {candidate.title || "Untitled Candidate"}
                                </span>

                                <span className="episode-list-id">
                                    {candidate.candidate_id}
                                </span>

                                <div className="candidate-details">

                    <div>
                        <span className="candidate-detail-label">
                            TOPICS
                        </span>

                        <span>
                            {candidate.topics?.length
                                ? candidate.topics.join(", ")
                                : "None"}
                        </span>
                    </div>

                    <div>
                        <span className="candidate-detail-label">
                            PARTICIPANTS
                        </span>

                        <span>
                            {candidate.participants?.length
                                ? candidate.participants.join(", ")
                                : "None"}
                        </span>
                    </div>

                    <div>
                        <span className="candidate-detail-label">
                            OBSERVATIONS
                        </span>

                        <span>
                    
                            {candidate.related_observations?.length || 0}
                        </span>
                    </div>

                    <div>
                        <span className="candidate-detail-label">
                            STATUS
                        </span>

                        <span>
                            {candidate.status || "candidate"}
                        </span>
                    </div>

                </div>

            </div>

        </div>

                        ))}

                    </div>

                )}

            </div>


            {/* =================================================
                RIGHT — SELECTED EPISODE
               ================================================= */}

            <div className="memory-detail-card">

                {!selectedEpisode ? (

                    <div className="memory-placeholder">

                        <div className="empty-symbol">
                            01
                        </div>

                        <h3>
                            Select an episode
                        </h3>

                        <p>
                            Choose an episode from the history
                            panel to inspect its stored memory
                            and observations.
                        </p>

                    </div>

                ) : (

                    <>

                        {/* EPISODE HEADER */}

                        <div className="memory-detail-header">

                            <div>

                                <span className="card-label">
                                    SELECTED MEMORY
                                </span>

                                <h3>
                                    {selectedEpisode.title ||
                                        "Untitled Episode"}
                                </h3>

                            </div>
                            <span style={{fontSize: "small"}}> {selectedEpisode.last_updated.split(" ")[0]}</span>
                            <span className="memory-episode-id">
                                {selectedEpisode.episode_id}
                            </span>

                        </div>


                        {/* EPISODE METADATA */}

                        <div className="memory-meta-grid">

                            <div className="memory-meta-item">

                                <span>
                                    TOPICS
                                </span>

                                <strong>
                                    {selectedEpisode.topics?.length
                                        ? selectedEpisode.topics.join(", ")
                                        : "None"}
                                </strong>

                            </div>


                            <div className="memory-meta-item">

                                <span>
                                    PARTICIPANTS
                                </span>

                                <strong>
                                    {selectedEpisode.participants?.length
                                        ? selectedEpisode.participants.join(", ")
                                        : "None"}
                                </strong>

                            </div>

                        </div>


                        {/* OBSERVATIONS */}

                        <div className="observations-section">

                            <div className="observations-header">

                                <div>

                                    <span className="card-label">
                                        RECORDED OBSERVATIONS
                                    </span>

                                    <h4>
                                        Conversation Memory
                                    </h4>

                                </div>

                                <span className="observation-count">
                                    {observations.length}
                                </span>

                            </div>


                            {observations.length === 0 ? (

                                <p className="empty-value">
                                    No observations found for this
                                    episode.
                                </p>

                            ) : (

                                <div className="observation-list">

                                    {observations.map(
                                        (observation, index) => (

                                            <div
                                                className="observation-item"
                                                key={observation.id}
                                            >

                                                <span className="observation-index">
                                                    {String(index + 1).padStart(
                                                        2,
                                                        "0"
                                                    )}
                                                </span>

                                                <div>

                                                    <span className="observation-id">
                                                        {observation.id}
                                                    </span>

                                                    <p>
                                                        {observation.text}
                                                    </p>

                                                </div>

                                            </div>

                                        )
                                    )}

                                </div>

                            )}

                        </div>

                    </>

                )}

            </div>

        </div>

    </section>
);
}

export default MemoryBrowser;
