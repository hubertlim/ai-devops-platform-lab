import "./StatusBar.css";

interface StatusBarProps {
  status: "connected" | "disconnected";
}

export function StatusBar({ status }: StatusBarProps) {
  return (
    <footer className="status-bar" role="status" aria-live="polite">
      <div className={`status-indicator status-indicator--${status}`} />
      <span className="status-text">
        API: {status === "connected" ? "Connected" : "Disconnected"}
      </span>
      <span className="status-provider">Provider: mock</span>
    </footer>
  );
}
