import { useState, useEffect, useRef } from "react";
import { apiClient, type CompletionResponse } from "../lib/api";
import "./ChatPanel.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  correlationId?: string;
  timestamp: Date;
}

interface ChatPanelProps {
  onStatusChange: (status: "connected" | "disconnected") => void;
}

export function ChatPanel({ onStatusChange }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Check API health on mount
    apiClient
      .healthCheck()
      .then(() => onStatusChange("connected"))
      .catch(() => onStatusChange("disconnected"));
  }, [onStatusChange]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response: CompletionResponse = await apiClient.complete(
        userMessage.content
      );

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.text,
        correlationId: response.correlation_id,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      onStatusChange("connected");
    } catch {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Failed to get response. Check that the API is running.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      onStatusChange("disconnected");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-messages" role="log" aria-live="polite">
        {messages.length === 0 && (
          <div className="chat-empty">
            <p>Send a message to the AI endpoint.</p>
            <p className="chat-hint">
              Try: &quot;hello&quot;, &quot;explain kubernetes&quot;, or
              &quot;what is devops&quot;
            </p>
          </div>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message chat-message--${msg.role}`}>
            <div className="chat-message-content">{msg.content}</div>
            {msg.correlationId && (
              <div className="chat-message-meta">
                ID: {msg.correlationId.slice(0, 8)}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="chat-message chat-message--assistant">
            <div className="chat-message-content chat-loading">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <label htmlFor="chat-input" className="sr-only">
          Enter your prompt
        </label>
        <input
          id="chat-input"
          type="text"
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a prompt..."
          disabled={isLoading}
          autoComplete="off"
        />
        <button
          type="submit"
          className="chat-submit"
          disabled={isLoading || !input.trim()}
          aria-label="Send message"
        >
          Send
        </button>
      </form>
    </div>
  );
}
