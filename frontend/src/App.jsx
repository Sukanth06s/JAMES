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
    <div className="app-shell">

        {/* =================================================
            HEADER
           ================================================= */}

        <header className="app-header">

            <div className="brand-row">

                <div className="brand-mark">

                    <div>
                        <h1>JAMES</h1>

                        <p>
                            Persistent Adaptive Assistant
                        </p>
                    </div>

                </div>


                <div className="system-status">

                    <span className="status-dot"></span>

                    System Ready

                </div>

            </div>

        </header>


        {/* =================================================
            NAVIGATION
           ================================================= */}

        <nav className="app-nav">

            <button
                className={`nav-item ${
                    activeView === "chat"
                        ? "active"
                        : ""
                }`}
                onClick={() => setActiveView("chat")}
            >
                Conversation
            </button>


            <button
                className={`nav-item ${
                    activeView === "signals"
                        ? "active"
                        : ""
                }`}
                onClick={() => setActiveView("signals")}
            >
                Signals
            </button>


            <button
                className={`nav-item ${
                    activeView === "episode"
                        ? "active"
                        : ""
                }`}
                onClick={() => setActiveView("episode")}
            >
                Current Episode
            </button>


            <button
                className={`nav-item ${
                    activeView === "memory"
                        ? "active"
                        : ""
                }`}
                onClick={() => setActiveView("memory")}
            >
                Memory & History
            </button>

        </nav>


        {/* =================================================
            MAIN CONTENT
           ================================================= */}

        <main className="main-content">

            {activeView === "chat" && (
                <Chat
                    onProcessed={setLastResult}
                />
            )}

            {activeView === "signals" && (
                <SignalPanel
                    result={lastResult}
                />
            )}

            {activeView === "episode" && (
                <EpisodePanel
                    result={lastResult}
                />
            )}

            {activeView === "memory" && (
                <MemoryBrowser />
            )}

        </main>


        {/* =================================================
            FOOTER
           ================================================= */}

        <footer className="app-footer">

            <span>
                JAMES Phase 2&nbsp;&nbsp;|&nbsp;&nbsp;
                Developer Interface
            </span>

            <span>
                Building Persistent AI for Real-world Use
            </span>

        </footer>

    </div>
);
}

export default App;