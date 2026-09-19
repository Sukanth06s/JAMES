import { useState } from "react";

import Chat from "./components/chat";
import SignalPanel from "./components/SignalPanel";
import EpisodePanel from "./components/EpisodePanel";
import MemoryBrowser from "./components/MemoryBrowser";

import "./App.css";

function App() {
  const [activeView, setActiveView] = useState("chat");
  const [lastResult, setLastResult] = useState(null);

  return (
    <div>
      <header>
        <h1>JAMES</h1>
        <p>Persistent Adaptive Assistant</p>

        <p>
          Last status:{" "}
          <strong>
            {lastResult?.status || "No message processed"}
          </strong>
        </p>
      </header>

      <nav>
        <button onClick={() => setActiveView("chat")}>
          Chat
        </button>

        <button onClick={() => setActiveView("signals")}>
          Signals
        </button>

        <button onClick={() => setActiveView("episode")}>
          Episode
        </button>

        <button onClick={() => setActiveView("memory")}>
          Memory
        </button>
      </nav>

      <main>
        {activeView === "chat" && (
          <Chat onProcessed={setLastResult} />
        )}

        {activeView === "signals" && (
          <SignalPanel result={lastResult} />
        )}

        {activeView === "episode" && (
          <EpisodePanel result={lastResult} />
        )}

        {activeView === "memory" && (
          <MemoryBrowser />
        )}
      </main>
    </div>
  );
}

export default App;