from __future__ import annotations

import json

import gradio as gr

from video_ai.admin_config import admin_snapshot, provider_status_rows, read_env_values, write_env_values
from video_ai.config import load_settings
from video_ai.runtime import clear_provider_cache, get_default_provider, list_providers, run_generation
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


def load_admin_values() -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
    values = read_env_values()
    return (
        values["DEFAULT_PROVIDER"],
        values["HF_SPACE_ID"],
        values["HF_API_NAME"],
        values["HF_TOKEN"],
        values["CLOUD_WEBHOOK_URL"],
        values["CLOUD_WEBHOOK_KEY"],
        values["GRADIO_SERVER_NAME"],
        values["GRADIO_SERVER_PORT"],
        values["AGNES_BASE_URL"],
        values["COMFYUI_BASE_URL"],
        admin_snapshot(),
    )


def save_admin_values(
    default_provider: str,
    hf_space_id: str,
    hf_api_name: str,
    hf_token: str,
    cloud_webhook_url: str,
    cloud_webhook_key: str,
    gradio_server_name: str,
    gradio_server_port: str,
    agnes_base_url: str,
    comfyui_base_url: str,
) -> tuple[str, list[list[str]], gr.Dropdown]:
    write_env_values(
        {
            "DEFAULT_PROVIDER": default_provider,
            "HF_SPACE_ID": hf_space_id,
            "HF_API_NAME": hf_api_name,
            "HF_TOKEN": hf_token,
            "CLOUD_WEBHOOK_URL": cloud_webhook_url,
            "CLOUD_WEBHOOK_KEY": cloud_webhook_key,
            "GRADIO_SERVER_NAME": gradio_server_name,
            "GRADIO_SERVER_PORT": gradio_server_port,
            "AGNES_BASE_URL": agnes_base_url,
            "COMFYUI_BASE_URL": comfyui_base_url,
        }
    )
    clear_provider_cache()
    return (
        "Configuração salva no arquivo .env. O cache de provedores foi limpo.",
        provider_status_rows(),
        gr.Dropdown(choices=list_providers(), value=get_default_provider()),
    )


def refresh_diagnostics() -> tuple[list[list[str]], str]:
    clear_provider_cache()
    return provider_status_rows(), admin_snapshot()


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Video AI") as demo:
        gr.Markdown(
            "# Video AI\n"
            "Hub visual para gerar vídeos com IA usando provedores plugáveis."
        )

        with gr.Tab("Gerar vídeo"):
            with gr.Row():
                with gr.Column(scale=1):
                    provider = gr.Dropdown(
                        choices=list_providers(),
                        value=get_default_provider(),
                        label="Provedor",
                    )
                    prompt = gr.Textbox(label="Prompt", value=DEFAULT_PROMPT, lines=5)
                    negative_prompt = gr.Textbox(
                        label="Prompt negativo",
                        value="texto distorcido, baixa qualidade, pessoas deformadas, flicker, blur excessivo",
                        lines=3,
                    )
                    image = gr.Image(label="Imagem de referência opcional", type="filepath")

                    with gr.Row():
                        duration = gr.Slider(1, 12, value=5, step=1, label="Duração em segundos")
                        seed = gr.Number(value=-1, precision=0, label="Seed (-1 = aleatória)")

                    with gr.Row():
                        width = gr.Dropdown([512, 576, 640, 768, 1024], value=768, label="Largura")
                        height = gr.Dropdown([288, 320, 432, 576, 768, 1024], value=432, label="Altura")

                    generate = gr.Button("Gerar vídeo", variant="primary")

                with gr.Column(scale=1):
                    video = gr.Video(label="Resultado")
                    log = gr.Code(label="Log", language="json")

            generate.click(
                fn=generate_video,
                inputs=[prompt, negative_prompt, provider, image, duration, width, height, seed],
                outputs=[video, log],
            )

        with gr.Tab("Provedores"):
            gr.Markdown(
                "Configure os provedores sem editar o `.env` manualmente. "
                "Depois de salvar, volte para a aba de geração e escolha o provedor."
            )

            values = read_env_values()
            default_provider = gr.Dropdown(
                choices=list_providers(),
                value=values["DEFAULT_PROVIDER"],
                label="Provedor padrão",
            )
            hf_space_id = gr.Textbox(value=values["HF_SPACE_ID"], label="HF_SPACE_ID")
            hf_api_name = gr.Textbox(value=values["HF_API_NAME"], label="HF_API_NAME")
            hf_token = gr.Textbox(value=values["HF_TOKEN"], label="HF_TOKEN", type="password")
            cloud_webhook_url = gr.Textbox(value=values["CLOUD_WEBHOOK_URL"], label="CLOUD_WEBHOOK_URL")
            cloud_webhook_key = gr.Textbox(value=values["CLOUD_WEBHOOK_KEY"], label="CLOUD_WEBHOOK_KEY", type="password")

            with gr.Accordion("Campos reservados para próximos provedores", open=False):
                agnes_base_url = gr.Textbox(value=values["AGNES_BASE_URL"], label="AGNES_BASE_URL")
                comfyui_base_url = gr.Textbox(value=values["COMFYUI_BASE_URL"], label="COMFYUI_BASE_URL")

            with gr.Accordion("Runtime", open=False):
                gradio_server_name = gr.Textbox(value=values["GRADIO_SERVER_NAME"], label="GRADIO_SERVER_NAME")
                gradio_server_port = gr.Textbox(value=values["GRADIO_SERVER_PORT"], label="GRADIO_SERVER_PORT")

            save_button = gr.Button("Salvar configuração", variant="primary")
            save_message = gr.Textbox(label="Status", interactive=False)

        with gr.Tab("Diagnóstico"):
            provider_table = gr.Dataframe(
                headers=["ID", "Nome", "Implementado", "Transporte", "Capacidades", "Credencial", "Endpoint"],
                value=provider_status_rows(),
                interactive=False,
                label="Catálogo de provedores",
            )
            snapshot = gr.Textbox(value=admin_snapshot(), label="Configuração carregada", lines=8)
            refresh = gr.Button("Atualizar diagnóstico")

        save_button.click(
            fn=save_admin_values,
            inputs=[
                default_provider,
                hf_space_id,
                hf_api_name,
                hf_token,
                cloud_webhook_url,
                cloud_webhook_key,
                gradio_server_name,
                gradio_server_port,
                agnes_base_url,
                comfyui_base_url,
            ],
            outputs=[save_message, provider_table, provider],
        )

        refresh.click(fn=refresh_diagnostics, outputs=[provider_table, snapshot])

    return demo


if __name__ == "__main__":
    settings = load_settings()
    app = build_app()
    app.launch(
        server_name=settings.gradio_server_name,
        server_port=settings.gradio_server_port,
    )
