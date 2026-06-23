from __future__ import annotations

from .providers.base import GenerationRequest, GenerationResult
from .providers.runtime_registry import provider_registry


def list_providers() -> list[str]:
    return provider_registry.available_provider_ids()


def get_default_provider() -> str:
    return provider_registry.get_default_provider_id()


def clear_provider_cache() -> None:
    provider_registry.clear()


def run_generation(provider_name: str, request: GenerationRequest) -> GenerationResult:
    return provider_registry.run_generation(provider_name, request)
