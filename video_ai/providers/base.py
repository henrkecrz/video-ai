from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass
class GenerationRequest:
    prompt: str
    negative_prompt: str = ""
    image_path: str | None = None
    duration_seconds: int = 5
    width: int = 768
    height: int = 432
    seed: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    ok: bool
    message: str
    video_path: str | None = None
    video_url: str | None = None
    raw: Any | None = None

    def best_output(self) -> str | None:
        if self.video_path and Path(self.video_path).exists():
            return self.video_path
        return self.video_url


class Provider(Protocol):
    name: str
    description: str

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate a video or return enough information for the UI to display the result."""
        raise NotImplementedError
