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
    <section>
      <h2>Episode Panel</h2>

      <div>
        <h3>Processing Status</h3>
        <p>{result.status || "unknown"}</p>
      </div>

      <div>
        <h3>Current Observation</h3>

        {observation ? (
          <>
            <p>
              <strong>ID:</strong> {observation.id}
            </p>

            <p>
              <strong>Text:</strong> {observation.text}
            </p>

            <p>
              <strong>Intent:</strong>{" "}
              {observation.intent || "None"}
            </p>
          </>
        ) : (
          <p>No observation was created.</p>
        )}
      </div>

      <div>
        <h3>Selected Episode</h3>

        {!episode ? (
          <p>No episode was created or matched.</p>
        ) : (
          <>
            <p>
              <strong>Episode ID:</strong>{" "}
              {episode.episode_id}
            </p>

            <p>
              <strong>Title:</strong>{" "}
              {episode.title || "Untitled"}
            </p>

            <p>
              <strong>Topics:</strong>{" "}
              {episode.topics?.length
                ? episode.topics.join(", ")
                : "None"}
            </p>

            <p>
              <strong>Participants:</strong>{" "}
              {episode.participants?.length
                ? episode.participants.join(", ")
                : "None"}
            </p>

            <p>
              <strong>Related Observations:</strong>{" "}
              {episode.related_observations?.length || 0}
            </p>
          </>
        )}
      </div>

      <div>
        <h3>Why This Episode?</h3>

        {result.status === "matched" ? (
          <p>
            This observation was associated with an
            existing episode by the current episode
            matching logic.
          </p>
        ) : result.status === "created" ? (
          <p>
            No existing episode was selected, so JAMES
            created a new episode for this observation.
          </p>
        ) : (
          <p>
            Episode selection information is not
            available.
          </p>
        )}
      </div>
    </section>
  );
}

export default EpisodePanel;