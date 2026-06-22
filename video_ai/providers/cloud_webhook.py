from __future__ import annotations

from typing import Any

import requests

from .base import GenerationRequest, GenerationResult


class CloudWebhookProvider:
    name = "cloud_webhook"
    description = "Adaptador genérico para APIs/webhooks que recebem prompt e retornam vídeo."

    def __init__(self, url: str, api_key: str = "") -> None:
        self.url = url.strip()
        self.api_key = api_key.strip()

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.url:
            return GenerationResult(
                ok=False,
                message="CLOUD_WEBHOOK_URL não foi configurado no arquivo .env.",
            )

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: dict[str, Any] = {
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "duration_seconds": request.duration_seconds,
            "width": request.width,
            "height": request.height,
            "seed": request.seed,
            "image_path": request.image_path,
            "extra": request.extra,
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=180)
            response.raise_for_status()
            data: Any = response.json()

            candidate = None
            if isinstance(data, dict):
                candidate = data.get("video_url") or data.get("video") or data.get("url") or data.get("path")

            video_url = candidate if isinstance(candidate, str) and candidate.startswith(("http://", "https://")) else None
            video_path = candidate if isinstance(candidate, str) and not video_url else None

            return GenerationResult(
                ok=True,
                message="Solicitação enviada ao provedor cloud.",
                video_path=video_path,
                video_url=video_url,
                raw=data,
            )
        except Exception as exc:  # noqa: BLE001
            return GenerationResult(
                ok=False,
                message=f"Erro ao chamar cloud webhook: {exc}",
            )
