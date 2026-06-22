from __future__ import annotations

import json

import gradio as gr

from video_ai.config import settings
from video_ai.orchestrator import get_default_provider, list_providers, run_generation
from video_ai.providers import GenerationRequest


DEFAULT_PROMPT = (
    "Vídeo institucional curto mostrando obras urbanas, equipes trabalhando, "
    "clima positivo, cidade organizada, estilo realista, movimento suave de câmera."
)


def generate_video(
    prompt: str,
    negative_prompt: str,
    provider_name: str,
    image_path: str | None,
    duration_seconds: int,
    width: int,
    height: int,
    seed: int,
) -> tuple[str | None, str]:
    seed_value = None if seed < 0 else seed

    request = GenerationRequest(
        prompt=prompt.strip(),
        negative_prompt=negative_prompt.strip(),
        image_path=image_path,
        duration_seconds=duration_seconds,
        width=width,
        height=height,
        seed=seed_value,
    )

    if not request.prompt:
        return None, "Digite um prompt antes de gerar."

    result = run_generation(provider_name, request)
    output = result.best_output()

    details = {
        "ok": result.ok,
        "message": result.message,
        "provider": provider_name,
        "video_path": result.video_path,
        "video_url": result.video_url,
        "raw": result.raw,
    }

    return output, json.dumps(details, indent=2, ensure_ascii=False)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Video AI") as demo:
        gr.Markdown(
            "# Video AI\n"
            "GUI inicial para testar geração de vídeos com IA usando provedores plugáveis."
        )

        with gr.Row():
            with gr.Column(scale=1):
                provider = gr.Dropdown(
                    choices=list_providers(),
                    value=get_default_provider(),
                    label="Provedor",
                )
                prompt = gr.Textbox(
                    label="Prompt",
                    value=DEFAULT_PROMPT,
                    lines=5,
                )
                negative_prompt = gr.Textbox(
                    label="Prompt negativo",
                    value="texto distorcido, baixa qualidade, pessoas deformadas, flicker, blur excessivo",
                    lines=3,
                )
                image = gr.Image(
                    label="Imagem de referência opcional",
                    type="filepath",
                )

                with gr.Row():
                    duration = gr.Slider(1, 12, value=5, step=1, label="Duração em segundos")
                    seed = gr.Number(value=-1, precision=0, label="Seed (-1 = aleatória)")

                with gr.Row():
                    width = gr.Dropdown([512, 576, 640, 768, 1024], value=768, label="Largura")
                    height = gr.Dropdown([288, 320, 432, 576, 768], value=432, label="Altura")

                generate = gr.Button("Gerar vídeo", variant="primary")

            with gr.Column(scale=1):
                video = gr.Video(label="Resultado")
                log = gr.Code(label="Log", language="json")

        gr.Markdown(
            "## Notas\n"
            "- Use `mock` para testar a interface sem API.\n"
            "- Use `huggingface_space` para conectar um Space público compatível com `gradio_client`.\n"
            "- Use `cloud_webhook` para conectar provedores gratuitos ou APIs próprias que retornem URL/arquivo de vídeo."
        )

        generate.click(
            fn=generate_video,
            inputs=[prompt, negative_prompt, provider, image, duration, width, height, seed],
            outputs=[video, log],
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name=settings.gradio_server_name,
        server_port=settings.gradio_server_port,
    )
