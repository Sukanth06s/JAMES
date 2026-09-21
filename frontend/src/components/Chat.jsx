import { useState  } from "react";
import { sendMessage } from "../services/api";

function Chat({onProcessed}){
    const [message,setMessage]=useState("");
    const [conversation,setConversation]=useState([]);
    const [loading,setLoading]=useState(false);
    const [error,setError]=useState("");

    async function handleSend(){
        if(!message.trim()|| loading){
            return;
        }
        const userMessage=message.trim();
        setLoading(true);
        setError("");

        try{
            const result=await sendMessage(
                userMessage,
                conversation
            );

            setConversation((previous)=>[
                ...previous,
                {
                    role:"user",
                    content:userMessage,
                },
                {
                    role:"assistant",
                    content:
                    result.extracted?.response ||
                    "JAMES processed the message.",
                },
            ]);
            setMessage("");

            onProcessed(result);
        } catch(err)
        {
            console.error(err);
            setError(err.message);
        } finally{
            setLoading(false);
        }
    }
    function handleKeyDown(event){
        if(event.key==="Enter" && !event.shiftKey){
            event.preventDefault();
            handleSend();
        }
    }

    return (
    <section className="chat-view">

        <div className="page-header">
            <div>
                <span className="section-label">
                    INTERACTION
                </span>

                <h2>Conversation</h2>

                <p>
                    Communicate with JAMES and observe the
                    current processing cycle.
                </p>
            </div>

            <div className="view-indicator">
                <span className="indicator-dot"></span>
                Active
            </div>
        </div>


        <div className="chat-container">

            <div className="chat-header">
                <div>
                    <strong>Conversation</strong>
                    <span>JAMES interaction history</span>
                </div>

                <span className="message-count">
                    {conversation.length}{" "}
                    {conversation.length === 1
                        ? "message"
                        : "messages"}
                </span>
            </div>


            <div className="chat-messages">

                {conversation.length === 0 && (
                    <div className="empty-conversation">

                        <div className="empty-symbol">
                            J
                        </div>

                        <h3>No conversation yet</h3>

                        <p>
                            Enter a message below to begin an
                            interaction with JAMES.
                        </p>

                    </div>
                )}


                {conversation.map((message, index) => (
                    <div
                        key={index}
                        className={`message-wrapper ${
                            message.role === "user"
                                ? "user-message"
                                : "james-message"
                        }`}
                    >
                        <div className="message-label">
                            {message.role === "user"
                                ? "YOU"
                                : "JAMES"}
                        </div>

                        <div className="message-bubble">
                            {message.content}
                        </div>
                    </div>
                ))}

            </div>


            {error && (
                <div className="chat-error">
                    <strong>Error:</strong>
                    <span>{error}</span>
                </div>
            )}


            <div className="chat-input-section">

                <textarea
                    value={message}
                    onChange={(event) =>
                        setMessage(event.target.value)
                    }
                    onKeyDown={handleKeyDown}
                    placeholder="Enter a message for JAMES..."
                    rows={3}
                    disabled={loading}
                />

                <div className="input-footer">

                    <span className="input-hint">
                        Enter to send · Shift + Enter for new line
                    </span>

                    <button
                        className="send-button"
                        onClick={handleSend}
                        disabled={
                            loading || !message.trim()
                        }
                    >
                        {loading ? "Processing..." : "Send"}
                    </button>

                </div>

            </div>

        </div>

    </section>
);
    
}

export default Chat;