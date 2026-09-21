function EpisodePanel({ result }) {
  if (!result) {
    return (
      <section>
        <h2>Episode Panel</h2>
        <p>No message has been processed yet.</p>
      </section>
    );
  }

  const episode = result.episode;
  const observation = result.observation;

  return (
    <section className="episode-view">

        <div className="page-header">
            <div>
                <span className="section-label">
                    CURRENT MEMORY STATE
                </span>

                <h2>Current Episode</h2>

                <p>
                    Inspect how JAMES handled the most recently
                    processed message.
                </p>
            </div>

            <div className="view-indicator">
                <span className="indicator-dot"></span>
                {result.status || "Unknown"}
            </div>
        </div>


        <div className="episode-grid">

            {/* CURRENT OBSERVATION */}
            <div className="episode-card">

                <div className="card-heading">
                    <span className="card-number">
                        01
                    </span>

                    <div>
                        <span className="card-label">
                            CURRENT OBSERVATION
                        </span>

                        <h3>
                            What JAMES recorded
                        </h3>
                    </div>
                </div>


                {observation ? (
                    <div className="episode-details">

                        <div className="detail-row">
                            <span>ID</span>
                            <strong>
                                {observation.id}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>TEXT</span>
                            <strong>
                                {observation.text}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>INTENT</span>
                            <strong>
                                {observation.intent || "None"}
                            </strong>
                        </div>

                    </div>
                ) : (
                    <p className="empty-value">
                        No observation was created.
                    </p>
                )}

            </div>


            {/* SELECTED EPISODE */}
            <div className="episode-card">

                <div className="card-heading">
                    <span className="card-number">
                        02
                    </span>

                    <div>
                        <span className="card-label">
                            SELECTED EPISODE
                        </span>

                        <h3>
                            Where JAMES placed it
                        </h3>
                    </div>
                </div>


                {!episode ? (
                    <p className="empty-value">
                        No episode was created or matched.
                    </p>
                ) : (
                    <div className="episode-details">

                        <div className="detail-row">
                            <span>EPISODE ID</span>
                            <strong>
                                {episode.episode_id}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>TITLE</span>
                            <strong>
                                {episode.title || "Untitled"}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>TOPICS</span>
                            <strong>
                                {episode.topics?.length
                                    ? episode.topics.join(", ")
                                    : "None"}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>PARTICIPANTS</span>
                            <strong>
                                {episode.participants?.length
                                    ? episode.participants.join(", ")
                                    : "None"}
                            </strong>
                        </div>

                        <div className="detail-row">
                            <span>OBSERVATIONS</span>
                            <strong>
                                {episode.related_observations?.length || 0}
                            </strong>
                        </div>

                    </div>
                )}

            </div>


            {/* PROCESSING DECISION */}
            <div className="episode-card full-width">

                <div className="card-heading">
                    <span className="card-number">
                        03
                    </span>

                    <div>
                        <span className="card-label">
                            PROCESSING DECISION
                        </span>

                        <h3>
                            What happened to this message?
                        </h3>
                    </div>
                </div>


                <div className="decision-panel">

                    {result.status === "matched" ? (
                        <>
                            <strong>
                                Existing episode selected
                            </strong>

                            <p>
                                This observation was associated
                                with an existing episode by the
                                current episode matching logic.
                            </p>
                        </>
                    ) : result.status === "created" ? (
                        <>
                            <strong>
                                New episode created
                            </strong>

                            <p>
                                No existing episode was selected,
                                so JAMES created a new episode for
                                this observation.
                            </p>
                        </>
                    ) : (
                        <>
                            <strong>
                                Episode selection unavailable
                            </strong>

                            <p>
                                Episode selection information is
                                not available for this result.
                            </p>
                        </>
                    )}

                </div>

            </div>

        </div>

    </section>
);
}

export default EpisodePanel;