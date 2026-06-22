from __future__ import annotations

from .config import settings
from .providers import (
    CloudWebhookProvider,
    GenerationRequest,
    GenerationResult,
    HuggingFaceSpaceProvider,
    MockProvider,
    Provider,
)


def build_providers() -> dict[str, Provider]:
    return {
        "mock": MockProvider(),
        "huggingface_space": HuggingFaceSpaceProvider(
            space_id=settings.hf_space_id,
            api_name=settings.hf_api_name,
            token=settings.hf_token,
        ),
        "cloud_webhook": CloudWebhookProvider(
            url=settings.cloud_webhook_url,
            api_key=settings.cloud_webhook_key,
        ),
    }


def list_providers() -> list[str]:
    return list(build_providers().keys())


def get_default_provider() -> str:
    providers = build_providers()
    if settings.default_provider in providers:
        return settings.default_provider
    return "mock"


def run_generation(provider_name: str, request: GenerationRequest) -> GenerationResult:
    providers = build_providers()
    provider = providers.get(provider_name)
    if provider is None:
        return GenerationResult(
            ok=False,
            message=f"Provedor desconhecido: {provider_name}",
        )
    return provider.generate(request)
