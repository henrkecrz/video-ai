from __future__ import annotations

from main import build_app
from video_ai.config import load_settings


if __name__ == "__main__":
    settings = load_settings()
    app = build_app()
    app.launch(
        server_name=settings.gradio_server_name,
        server_port=settings.gradio_server_port,
    )
