from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "mock")

    hf_space_id: str = os.getenv("HF_SPACE_ID", "")
    hf_api_name: str = os.getenv("HF_API_NAME", "/predict")
    hf_token: str = os.getenv("HF_TOKEN", "")

    cloud_webhook_url: str = os.getenv("CLOUD_WEBHOOK_URL", "")
    cloud_webhook_key: str = os.getenv("CLOUD_WEBHOOK_KEY", "")

    gradio_server_name: str = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    gradio_server_port: int = int(os.getenv("GRADIO_SERVER_PORT", "7860"))


settings = Settings()
