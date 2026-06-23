from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TransportType = Literal[
    "local",
    "gradio_space",
    "http_webhook",
    "comfyui",
    "future",
]


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    """Metadados neutros de um provedor.

    A implementação concreta fica em `video_ai.providers`. Este catálogo existe para
    que a UI, o registry e a documentação leiam a mesma fonte de verdade.
    """

    provider_id: str
    label: str
    transport_type: TransportType
    capabilities: tuple[str, ...]
    credential_env: str | None = None
    base_url_env: str | None = None
    default_base_url: str | None = None
    implemented: bool = True
    description: str = ""
    docs_url: str = ""


PROVIDER_CATALOG: dict[str, ProviderDescriptor] = {
    "mock": ProviderDescriptor(
        provider_id="mock",
        label="Mock local",
        transport_type="local",
        capabilities=("test", "offline", "no_api_key"),
        description="Valida a interface sem chamar serviços externos.",
    ),
    "huggingface_space": ProviderDescriptor(
        provider_id="huggingface_space",
        label="Hugging Face Space",
        transport_type="gradio_space",
        capabilities=("text_to_video", "image_to_video", "free_tier", "cloud"),
        credential_env="HF_TOKEN",
        base_url_env="HF_SPACE_ID",
        description=(
            "Conecta Spaces públicos/privados compatíveis com gradio_client. "
            "Cada Space pode exigir assinatura própria de parâmetros."
        ),
        docs_url="https://huggingface.co/docs/hub/spaces",
    ),
    "cloud_webhook": ProviderDescriptor(
        provider_id="cloud_webhook",
        label="Cloud webhook genérico",
        transport_type="http_webhook",
        capabilities=("text_to_video", "image_to_video", "cloud", "custom_api"),
        credential_env="CLOUD_WEBHOOK_KEY",
        base_url_env="CLOUD_WEBHOOK_URL",
        description=(
            "Adaptador para APIs próprias, n8n, Colab, Kaggle, RunPod, Vast ou "
            "qualquer endpoint HTTP que retorne uma URL/caminho de vídeo."
        ),
    ),
    "agnes": ProviderDescriptor(
        provider_id="agnes",
        label="Agnes / API gratuita futura",
        transport_type="future",
        capabilities=("text_to_video", "image_to_video", "cloud", "free_tier"),
        credential_env="AGNES_API_KEY",
        base_url_env="AGNES_BASE_URL",
        implemented=False,
        description=(
            "Reservado para um adaptador específico da Agnes quando a API estável "
            "e a assinatura de geração forem confirmadas."
        ),
    ),
    "comfyui": ProviderDescriptor(
        provider_id="comfyui",
        label="ComfyUI remoto/local",
        transport_type="comfyui",
        capabilities=("workflow", "text_to_video", "image_to_video", "local", "remote"),
        base_url_env="COMFYUI_BASE_URL",
        default_base_url="http://127.0.0.1:8188",
        implemented=False,
        description=(
            "Reservado para executar workflows JSON do ComfyUI com Wan, LTX, "
            "HunyuanVideo ou outros modelos."
        ),
    ),
    "colab_kaggle": ProviderDescriptor(
        provider_id="colab_kaggle",
        label="Colab/Kaggle via webhook",
        transport_type="future",
        capabilities=("notebook", "free_tier", "gpu", "cloud"),
        implemented=False,
        description=(
            "Estratégia futura: notebook com endpoint temporário ligado pelo "
            "CloudWebhookProvider."
        ),
    ),
    "replicate_fal": ProviderDescriptor(
        provider_id="replicate_fal",
        label="Replicate/Fal fallback",
        transport_type="future",
        capabilities=("paid_fallback", "cloud", "api"),
        implemented=False,
        description="Fallback futuro para qualidade/velocidade quando o custo for aceitável.",
    ),
}


IMPLEMENTED_PROVIDER_IDS: tuple[str, ...] = tuple(
    provider_id
    for provider_id, descriptor in PROVIDER_CATALOG.items()
    if descriptor.implemented
)

ALL_PROVIDER_IDS: tuple[str, ...] = tuple(PROVIDER_CATALOG.keys())


if len(set(ALL_PROVIDER_IDS)) != len(ALL_PROVIDER_IDS):
    raise AssertionError("Duplicate provider ids in PROVIDER_CATALOG")
