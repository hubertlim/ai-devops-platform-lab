import { useState } from "react";
import { ChatPanel } from "./components/ChatPanel";
import { StatusBar } from "./components/StatusBar";
import "./App.css";

function App() {
  const [apiStatus, setApiStatus] = useState<"connected" | "disconnected">(
    "disconnected"
  );

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI DevOps Platform Lab</h1>
        <p className="app-subtitle">
          Full-stack AI application with production-grade DevOps
        </p>
      </header>

      <main className="app-main">
        <ChatPanel onStatusChange={setApiStatus} />
      </main>

      <StatusBar status={apiStatus} />
    </div>
  );
}

export default App;
