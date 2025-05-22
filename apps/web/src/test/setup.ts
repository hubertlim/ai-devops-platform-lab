import "@testing-library/jest-dom";

// jsdom doesn't implement scrollIntoView
Element.prototype.scrollIntoView = () => {};

// Mock fetch for components that call the API on mount
globalThis.fetch = async () =>
  ({
    ok: true,
    json: async () => ({ status: "healthy", service: "test", version: "0.1.0", environment: "test" }),
  }) as Response;
