function SignalPanel({result}){
    if(!result)
    {
        return(
            <section>
                <h2>Signal Panel</h2>
                <p>No message has been processed yet.</p>
            </section>
        );
    }
    const extracted=result.extracted ||{};
    return (
    <section className="signals-view">

        <div className="page-header">

            <div>
                <span className="section-label">
                    EXTRACTED SIGNALS
                </span>

                <h2>Signal Analysis</h2>

                <p>
                    Inspect the signals extracted from the
                    most recently processed message.
                </p>
            </div>

            <div className="view-indicator">
                <span className="indicator-dot"></span>
                Processed
            </div>

        </div>


        <div className="signals-grid">

            {/* TOPICS */}

            <div className="signal-card">

                <div className="card-heading">

                    <span className="card-number">
                        01
                    </span>

                    <div>
                        <span className="card-label">
                            TOPIC SIGNALS
                        </span>

                        <h3>
                            Topics
                        </h3>
                    </div>

                </div>


                {extracted.topics?.length > 0 ? (

                    <div className="signal-tags">

                        {extracted.topics.map(
                            (topic, index) => (
                                <span
                                    className="signal-tag"
                                    key={index}
                                >
                                    {topic}
                                </span>
                            )
                        )}

                    </div>

                ) : (

                    <p className="empty-value">
                        None detected.
                    </p>

                )}

            </div>


            {/* INTENT */}

            <div className="signal-card">

                <div className="card-heading">

                    <span className="card-number">
                        02
                    </span>

                    <div>
                        <span className="card-label">
                            INTENT SIGNAL
                        </span>

                        <h3>
                            Intent
                        </h3>
                    </div>

                </div>


                <div className="signal-value">
                    {extracted.intent || "None"}
                </div>

            </div>


            {/* SUMMARY */}

            <div className="signal-card full-width">

                <div className="card-heading">

                    <span className="card-number">
                        03
                    </span>

                    <div>
                        <span className="card-label">
                            MESSAGE INTERPRETATION
                        </span>

                        <h3>
                            Summary
                        </h3>
                    </div>

                </div>


                <div className="signal-text">
                    {extracted.summary || "None"}
                </div>

            </div>


            {/* TAKEAWAY */}

            <div className="signal-card full-width">

                <div className="card-heading">

                    <span className="card-number">
                        04
                    </span>

                    <div>
                        <span className="card-label">
                            RETAINED INSIGHT
                        </span>

                        <h3>
                            Takeaway
                        </h3>
                    </div>

                </div>


                <div className="signal-text">
                    {extracted.takeaway || "None"}
                </div>

            </div>

        </div>

    </section>
);
}

export default SignalPanel;