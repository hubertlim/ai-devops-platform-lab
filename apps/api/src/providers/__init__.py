"""AI provider factory."""

from src.providers.base import AIProvider
from src.providers.mock import MockProvider


def get_provider(provider_name: str) -> AIProvider:
    """Return the configured AI provider instance."""
    providers: dict[str, type[AIProvider]] = {
        "mock": MockProvider,
    }

    provider_class = providers.get(provider_name)
    if not provider_class:
        msg = f"Unknown AI provider: {provider_name}. Available: {list(providers.keys())}"
        raise ValueError(msg)

    return provider_class()
