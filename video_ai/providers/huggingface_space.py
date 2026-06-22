from __future__ import annotations

from typing import Any

from gradio_client import Client

from .base import GenerationRequest, GenerationResult


class HuggingFaceSpaceProvider:
    name = "huggingface_space"
    description = "Envia o prompt para um Hugging Face Space compatível com gradio_client."

    def __init__(self, space_id: str, api_name: str = "/predict", token: str = "") -> None:
        self.space_id = space_id.strip()
        self.api_name = api_name.strip() or "/predict"
        self.token = token.strip() or None

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.space_id:
            return GenerationResult(
                ok=False,
                message="HF_SPACE_ID não foi configurado no arquivo .env.",
            )

        try:
            client = Client(self.space_id, hf_token=self.token)

            # Cada Space pode ter assinatura diferente. Começamos com um payload simples.
            # Para Spaces específicos, ajuste HF_API_NAME e/ou este adaptador.
            result: Any = client.predict(
                request.prompt,
                api_name=self.api_name,
            )

            video_path = None
            video_url = None

            if isinstance(result, str):
                if result.startswith("http://") or result.startswith("https://"):
                    video_url = result
                else:
                    video_path = result
            elif isinstance(result, dict):
                candidate = result.get("video") or result.get("url") or result.get("path")
                if isinstance(candidate, str):
                    if candidate.startswith("http://") or candidate.startswith("https://"):
                        video_url = candidate
                    else:
                        video_path = candidate

            return GenerationResult(
                ok=True,
                message="Solicitação enviada ao Hugging Face Space. Verifique o resultado abaixo.",
                video_path=video_path,
                video_url=video_url,
                raw=result,
            )
        except Exception as exc:  # noqa: BLE001
            return GenerationResult(
                ok=False,
                message=f"Erro ao chamar Hugging Face Space: {exc}",
            )
