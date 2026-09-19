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
    return(
        <section>
            <h2>Signal Panel</h2>

            <div>
                <h3>Topics</h3>
                {extracted.topics?.length>0?(
                    <ul>
                        {extracted.topics.map((topic,index)=>(
                            <li key={index}>{topic}</li>
                        ))}
                    </ul>
                ):(
                    <p>None</p>
                )}
            </div>
            
            <div>
                <h3>Intent</h3>
                <p>{extracted.intent || "None"}</p>
            </div>

            <div>
                <h3>Summary</h3>
                <p>{extracted.summary || "None"}</p>
            </div>

            <div>
                <h3>Takeaway</h3>
                <p>{extracted.takeaway || "None"}</p>
            </div>
        </section>
    );
}

export default SignalPanel;