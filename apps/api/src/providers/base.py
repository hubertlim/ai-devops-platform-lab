"""Base class for AI providers."""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI completion providers."""

    @abstractmethod
    async def complete(self, prompt: str, max_tokens: int, temperature: float) -> dict:
        """Generate a completion.

        Returns:
            dict with keys: text, model, usage
        """
        ...
