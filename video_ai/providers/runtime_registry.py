from __future__ import annotations

from video_ai.config import load_settings
from video_ai.provider_catalog import IMPLEMENTED_PROVIDER_IDS
from video_ai.providers.base import GenerationRequest, GenerationResult
from video_ai.providers.cloud_webhook import CloudWebhookProvider
from video_ai.providers.huggingface_space import HuggingFaceSpaceProvider
from video_ai.providers.mock import MockProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers = {}

    def available_provider_ids(self) -> list[str]:
        return list(IMPLEMENTED_PROVIDER_IDS)

    def get_default_provider_id(self) -> str:
        settings = load_settings()
        return settings.default_provider if settings.default_provider in IMPLEMENTED_PROVIDER_IDS else "mock"

    def clear(self) -> None:
        self._providers.clear()

    def get(self, provider_id: str):
        if provider_id not in IMPLEMENTED_PROVIDER_IDS:
            raise ValueError(f"Provedor indisponível: {provider_id}")
        if provider_id not in self._providers:
            settings = load_settings()
            if provider_id == "mock":
                self._providers[provider_id] = MockProvider()
            elif provider_id == "huggingface_space":
                self._providers[provider_id] = HuggingFaceSpaceProvider(settings.hf_space_id, settings.hf_api_name, settings.hf_token)
            elif provider_id == "cloud_webhook":
                self._providers[provider_id] = CloudWebhookProvider(settings.cloud_webhook_url, settings.cloud_webhook_key)
        return self._providers[provider_id]

    def run_generation(self, provider_id: str, request: GenerationRequest) -> GenerationResult:
        try:
            return self.get(provider_id).generate(request)
        except Exception as exc:
            return GenerationResult(ok=False, message=str(exc))


provider_registry = ProviderRegistry()
