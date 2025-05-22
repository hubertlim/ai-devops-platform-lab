"""Mock AI provider for development and testing."""

import asyncio
import hashlib

from src.providers.base import AIProvider

# Predefined responses for common prompts (deterministic for testing)
MOCK_RESPONSES = {
    "hello": (
        "Hello! I'm the AI DevOps Platform Lab mock provider. "
        "I can help you test the system without requiring real API keys."
    ),
    "explain kubernetes": (
        "Kubernetes is a container orchestration platform that automates "
        "deployment, scaling, and management of containerized applications. "
        "It groups containers into logical units for easy management and discovery."
    ),
    "what is devops": (
        "DevOps is a set of practices combining software development (Dev) and "
        "IT operations (Ops). It aims to shorten the development lifecycle while "
        "delivering features, fixes, and updates frequently in close alignment "
        "with business objectives."
    ),
}


class MockProvider(AIProvider):
    """Mock AI provider that returns deterministic responses."""

    async def complete(self, prompt: str, max_tokens: int, temperature: float) -> dict:
        """Generate a mock completion with simulated latency."""
        # Simulate realistic API latency (50-200ms)
        await asyncio.sleep(0.05 + (len(prompt) % 150) / 1000)

        # Check for predefined responses
        prompt_lower = prompt.lower().strip()
        for key, response in MOCK_RESPONSES.items():
            if key in prompt_lower:
                text = response
                break
        else:
            # Generate a deterministic response based on prompt hash
            prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:8]
            text = (
                f"[Mock Response {prompt_hash}] This is a simulated AI response to: "
                f"'{prompt[:100]}'. In production, this would be handled by the configured "
                f"LLM provider (OpenAI, Anthropic, or Ollama). "
                f"Temperature: {temperature}, Max tokens: {max_tokens}."
            )

        # Simulate token counting
        prompt_tokens = len(prompt.split())
        completion_tokens = len(text.split())

        return {
            "text": text,
            "model": "mock-v1",
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }
