from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


ENV_FILE = Path(".env")


def _load_env() -> None:
    load_dotenv(ENV_FILE, override=True)


def _int_env(key: str, default: int) -> int:
    value = os.getenv(key, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    default_provider: str = "mock"

    hf_space_id: str = ""
    hf_api_name: str = "/predict"
    hf_token: str = ""

    cloud_webhook_url: str = ""
    cloud_webhook_key: str = ""

    agnes_api_key: str = ""
    agnes_base_url: str = ""
    comfyui_base_url: str = "http://127.0.0.1:8188"

    gradio_server_name: str = "127.0.0.1"
    gradio_server_port: int = 7860

    provider_timeout_seconds: int = 180
    provider_max_concurrency: int = 2


def load_settings() -> Settings:
    """Load settings from .env and process environment.

    The app calls this at runtime so changes made by the Admin tab can be applied
    without editing Python code.
    """

    _load_env()
    return Settings(
        default_provider=os.getenv("DEFAULT_PROVIDER", "mock"),
        hf_space_id=os.getenv("HF_SPACE_ID", ""),
        hf_api_name=os.getenv("HF_API_NAME", "/predict"),
        hf_token=os.getenv("HF_TOKEN", ""),
        cloud_webhook_url=os.getenv("CLOUD_WEBHOOK_URL", ""),
        cloud_webhook_key=os.getenv("CLOUD_WEBHOOK_KEY", ""),
        agnes_api_key=os.getenv("AGNES_API_KEY", ""),
        agnes_base_url=os.getenv("AGNES_BASE_URL", ""),
        comfyui_base_url=os.getenv("COMFYUI_BASE_URL", "http://127.0.0.1:8188"),
        gradio_server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        gradio_server_port=_int_env("GRADIO_SERVER_PORT", 7860),
        provider_timeout_seconds=_int_env("PROVIDER_TIMEOUT_SECONDS", 180),
        provider_max_concurrency=_int_env("PROVIDER_MAX_CONCURRENCY", 2),
    )


settings = load_settings()
