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

    return(
        <section>
      <h2>Chat</h2>

      <div>
        {conversation.length === 0 && (
          <p>No conversation yet.</p>
        )}

        {conversation.map((message, index) => (
          <div key={index}>
            <strong>
              {message.role === "user"
                ? "You"
                : "JAMES"}
            </strong>

            <p>{message.content}</p>
          </div>
        ))}
      </div>

      {error && (
        <p>
          <strong>Error:</strong> {error}
        </p>
      )}

      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Enter a message..."
        rows={3}
        disabled={loading}
      />

      <button
        onClick={handleSend}
        disabled={loading || !message.trim()}
      >
        {loading ? "Processing..." : "Send"}
      </button>
    </section>
  );
    
}

export default Chat;