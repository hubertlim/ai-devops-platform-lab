/**
 * API client for the AI DevOps Platform backend.
 * Includes correlation ID propagation for distributed tracing.
 */

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface CompletionResponse {
  text: string;
  provider: string;
  model: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  correlation_id: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
}

function generateCorrelationId(): string {
  return crypto.randomUUID();
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const correlationId = generateCorrelationId();

    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        "X-Correlation-ID": correlationId,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>("/health");
  }

  async complete(
    prompt: string,
    maxTokens = 256,
    temperature = 0.7
  ): Promise<CompletionResponse> {
    return this.request<CompletionResponse>("/api/v1/completions", {
      method: "POST",
      body: JSON.stringify({
        prompt,
        max_tokens: maxTokens,
        temperature,
      }),
    });
  }
}

export const apiClient = new ApiClient(API_URL);
