from __future__ import annotations

from collections.abc import Callable

from video_ai.config import Settings, load_settings
from video_ai.provider_catalog import IMPLEMENTED_PROVIDER_IDS, PROVIDER_CATALOG, ProviderDescriptor
from video_ai.providers.base import GenerationRequest, GenerationResult, Provider
from video_ai.providers.cloud_webhook import CloudWebhookProvider
from video_ai.providers.huggingface_space import HuggingFaceSpaceProvider
from video_ai.providers.mock import MockProvider


ProviderFactory = Callable[[Settings, ProviderDescriptor], Provider]


def _create_mock(_settings: Settings, _descriptor: ProviderDescriptor) -> Provider:
    return MockProvider()


def _create_huggingface_space(settings: Settings, _descriptor: ProviderDescriptor) -> Provider:
    return HuggingFaceSpaceProvider(
        space_id=settings.hf_space_id,
        api_name=settings.hf_api_name,
        token=settings.hf_token,
    )


def _create_cloud_webhook(settings: Settings, _descriptor: ProviderDescriptor) -> Provider:
    return CloudWebhookProvider(
        url=settings.cloud_webhook_url,
        api_key=settings.cloud_webhook_key,
        timeout_seconds=settings.provider_timeout_seconds,
    )


PROVIDER_FACTORIES: dict[str, ProviderFactory] = {
    "mock": _create_mock,
    "huggingface_space": _create_huggingface_space,
    "cloud_webhook": _create_cloud_webhook,
}


if set(PROVIDER_FACTORIES) != set(IMPLEMENTED_PROVIDER_IDS):
    raise AssertionError(
        "PROVIDER_FACTORIES and IMPLEMENTED_PROVIDER_IDS are out of sync: "
        f"factories={set(PROVIDER_FACTORIES)!r} implemented={set(IMPLEMENTED_PROVIDER_IDS)!r}"
    )


class ProviderRegistry:
    """Runtime cache for providers.

    Providers are built lazily so opening the GUI does not initialize cloud clients,
    network sessions or future heavy local backends until the user actually uses
    them.
    """

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def available_provider_ids(self) -> list[str]:
        return list(IMPLEMENTED_PROVIDER_IDS)

    def get_default_provider_id(self) -> str:
        settings = load_settings()
        if settings.default_provider in IMPLEMENTED_PROVIDER_IDS:
            return settings.default_provider
        return "mock"

    def clear(self) -> None:
        self._providers.clear()

    def get(self, provider_id: str) -> Provider:
        if provider_id not in IMPLEMENTED_PROVIDER_IDS:
            known = ", ".join(IMPLEMENTED_PROVIDER_IDS)
            raise ValueError(f"Provedor não implementado ou desconhecido: {provider_id}. Disponíveis: {known}")

        if provider_id not in self._providers:
            settings = load_settings()
            descriptor = PROVIDER_CATALOG[provider_id]
            factory = PROVIDER_FACTORIES[provider_id]
            self._providers[provider_id] = factory(settings, descriptor)

        return self._providers[provider_id]

    def run_generation(self, provider_id: str, request: GenerationRequest) -> GenerationResult:
        try:
            provider = self.get(provider_id)
        except Exception as exc:  # noqa: BLE001
            return GenerationResult(ok=False, message=str(exc))
        return provider.generate(request)


provider_registry = ProviderRegistry()
