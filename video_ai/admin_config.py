from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import dotenv_values

from .config import ENV_FILE, load_settings
from .provider_catalog import IMPLEMENTED_PROVIDER_IDS, PROVIDER_CATALOG


FieldType = Literal["text", "secret", "number", "select", "textarea"]


@dataclass(frozen=True, slots=True)
class ConfigSectionSpec:
    section_id: str
    label: str
    description: str


@dataclass(frozen=True, slots=True)
class ConfigFieldSpec:
    key: str
    label: str
    section_id: str
    field_type: FieldType = "text"
    default: str = ""
    options: tuple[str, ...] = ()
    description: str = ""


SECTIONS: tuple[ConfigSectionSpec, ...] = (
    ConfigSectionSpec(
        "providers",
        "Provedores",
        "Chaves, Spaces, URLs e endpoints usados para geração.",
    ),
    ConfigSectionSpec(
        "runtime",
        "Runtime",
        "Configurações da interface e limites de execução.",
    ),
    ConfigSectionSpec(
        "future",
        "Futuros backends",
        "Campos reservados para Agnes, ComfyUI e outros provedores.",
    ),
)


FIELDS: tuple[ConfigFieldSpec, ...] = (
    ConfigFieldSpec(
        "DEFAULT_PROVIDER",
        "Provedor padrão",
        "providers",
        "select",
        default="mock",
        options=IMPLEMENTED_PROVIDER_IDS,
        description="Provedor inicial selecionado na aba de geração.",
    ),
    ConfigFieldSpec(
        "HF_SPACE_ID",
        "Hugging Face Space ID",
        "providers",
        default="",
        description="Exemplo: usuario/space-name. Usado pelo HuggingFaceSpaceProvider.",
    ),
    ConfigFieldSpec(
        "HF_API_NAME",
        "Hugging Face API name",
        "providers",
        default="/predict",
        description="Rota Gradio do Space. Muitos Spaces usam /predict.",
    ),
    ConfigFieldSpec(
        "HF_TOKEN",
        "Hugging Face token",
        "providers",
        "secret",
        default="",
        description="Opcional para Spaces públicos; útil para privados ou com autenticação.",
    ),
    ConfigFieldSpec(
        "CLOUD_WEBHOOK_URL",
        "Cloud webhook URL",
        "providers",
        default="",
        description="Endpoint HTTP que recebe JSON e retorna video_url/video/url/path.",
    ),
    ConfigFieldSpec(
        "CLOUD_WEBHOOK_KEY",
        "Cloud webhook key",
        "providers",
        "secret",
        default="",
        description="Token Bearer opcional para o webhook.",
    ),
    ConfigFieldSpec(
        "GRADIO_SERVER_NAME",
        "Host Gradio",
        "runtime",
        default="127.0.0.1",
    ),
    ConfigFieldSpec(
        "GRADIO_SERVER_PORT",
        "Porta Gradio",
        "runtime",
        "number",
        default="7860",
    ),
    ConfigFieldSpec(
        "PROVIDER_TIMEOUT_SECONDS",
        "Timeout do provedor",
        "runtime",
        "number",
        default="180",
        description="Tempo máximo de espera para webhooks HTTP.",
    ),
    ConfigFieldSpec(
        "PROVIDER_MAX_CONCURRENCY",
        "Concorrência máxima",
        "runtime",
        "number",
        default="2",
        description="Reservado para fila/execução futura.",
    ),
    ConfigFieldSpec(
        "AGNES_API_KEY",
        "Agnes API key",
        "future",
        "secret",
        default="",
        description="Reservado para futuro AgnesProvider.",
    ),
    ConfigFieldSpec(
        "AGNES_BASE_URL",
        "Agnes base URL",
        "future",
        default="",
        description="Reservado para futuro AgnesProvider.",
    ),
    ConfigFieldSpec(
        "COMFYUI_BASE_URL",
        "ComfyUI base URL",
        "future",
        default="http://127.0.0.1:8188",
        description="Reservado para futuro ComfyUIProvider.",
    ),
)


FIELD_BY_KEY: dict[str, ConfigFieldSpec] = {field.key: field for field in FIELDS}


def read_env_values(path: Path = ENV_FILE) -> dict[str, str]:
    raw = dotenv_values(path) if path.exists() else {}
    values = {field.key: field.default for field in FIELDS}
    for key, value in raw.items():
        if key in values and value is not None:
            values[key] = str(value)
    return values


def write_env_values(values: dict[str, str], path: Path = ENV_FILE) -> None:
    current = read_env_values(path)
    current.update({key: str(value) for key, value in values.items() if key in FIELD_BY_KEY})

    lines: list[str] = [
        "# Video AI - configuração gerenciada pela aba Provedores",
        "# Edite pela interface ou manualmente se preferir.",
        "",
    ]

    for section in SECTIONS:
        lines.append(f"# {section.label}")
        for field in FIELDS:
            if field.section_id != section.section_id:
                continue
            value = current.get(field.key, field.default)
            value = value.replace("\n", " ").strip()
            lines.append(f"{field.key}={value}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def provider_status_rows() -> list[list[str]]:
    settings = load_settings()
    rows: list[list[str]] = []

    env_values = {
        "HF_SPACE_ID": settings.hf_space_id,
        "HF_TOKEN": settings.hf_token,
        "CLOUD_WEBHOOK_URL": settings.cloud_webhook_url,
        "CLOUD_WEBHOOK_KEY": settings.cloud_webhook_key,
        "AGNES_API_KEY": settings.agnes_api_key,
        "AGNES_BASE_URL": settings.agnes_base_url,
        "COMFYUI_BASE_URL": settings.comfyui_base_url,
    }

    for descriptor in PROVIDER_CATALOG.values():
        credential_status = "não exige"
        if descriptor.credential_env:
            credential_status = "configurado" if env_values.get(descriptor.credential_env) else "pendente"

        endpoint_status = "não exige"
        if descriptor.base_url_env:
            endpoint_status = "configurado" if env_values.get(descriptor.base_url_env) else "pendente"

        rows.append(
            [
                descriptor.provider_id,
                descriptor.label,
                "sim" if descriptor.implemented else "planejado",
                descriptor.transport_type,
                ", ".join(descriptor.capabilities),
                credential_status,
                endpoint_status,
            ]
        )

    return rows


def admin_snapshot() -> str:
    settings = load_settings()
    return (
        "Configuração carregada:\n"
        f"- Provedor padrão: {settings.default_provider}\n"
        f"- HF Space: {settings.hf_space_id or 'não configurado'}\n"
        f"- Webhook cloud: {settings.cloud_webhook_url or 'não configurado'}\n"
        f"- ComfyUI URL futura: {settings.comfyui_base_url}\n"
        f"- Gradio: {settings.gradio_server_name}:{settings.gradio_server_port}\n"
    )
