import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders the application title", () => {
    render(<App />);
    expect(screen.getByText("AI DevOps Platform Lab")).toBeInTheDocument();
  });

  it("renders the status bar", () => {
    render(<App />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("renders the chat input", () => {
    render(<App />);
    expect(
      screen.getByPlaceholderText("Type a prompt...")
    ).toBeInTheDocument();
  });

  it("has an accessible send button", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: /send/i })).toBeInTheDocument();
  });
});
