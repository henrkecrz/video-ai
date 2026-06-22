from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .base import GenerationRequest, GenerationResult


class MockProvider:
    name = "mock"
    description = "Modo de teste: valida a interface sem chamar API externa."

    def generate(self, request: GenerationRequest) -> GenerationResult:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        prompt_file = output_dir / f"mock-{stamp}.txt"
        prompt_file.write_text(
            "Video AI mock generation\n\n"
            f"Prompt: {request.prompt}\n"
            f"Negative prompt: {request.negative_prompt}\n"
            f"Duration: {request.duration_seconds}s\n"
            f"Size: {request.width}x{request.height}\n"
            f"Seed: {request.seed}\n",
            encoding="utf-8",
        )

        return GenerationResult(
            ok=True,
            message=(
                "Fluxo executado em modo teste. Nenhum vídeo foi gerado, "
                f"mas o prompt foi salvo em {prompt_file}."
            ),
            video_path=None,
            raw={"prompt_file": str(prompt_file)},
        )
