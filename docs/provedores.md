# Provedores e caminhos de geração

Este documento registra os caminhos que o projeto deve suportar para gerar vídeos com IA usando GUI e, quando possível, processamento gratuito em nuvem.

## 1. Hugging Face Spaces

Uso principal: testar modelos gratuitos/abertos em Spaces públicos.

Exemplos de modelos/projetos para investigar:

- Wan 2.1 / Wan 2.2;
- LTX Video;
- HunyuanVideo;
- demos públicas com ZeroGPU;
- Spaces com API Gradio aberta.

Configuração no `.env`:

```env
DEFAULT_PROVIDER=huggingface_space
HF_SPACE_ID=usuario/space-name
HF_API_NAME=/predict
HF_TOKEN=
```

Observações:

- Cada Space pode ter uma assinatura diferente de entrada.
- O adaptador inicial envia apenas o prompt.
- Para produção, criar adaptadores específicos por Space/modelo.

## 2. Cloud webhook genérico

Uso principal: conectar APIs gratuitas, servidores próprios, automações n8n, Colab, Kaggle, RunPod, Vast ou qualquer endpoint que aceite JSON.

Payload enviado:

```json
{
  "prompt": "texto do prompt",
  "negative_prompt": "texto negativo",
  "duration_seconds": 5,
  "width": 768,
  "height": 432,
  "seed": null,
  "image_path": null,
  "extra": {}
}
```

Resposta esperada:

```json
{
  "video_url": "https://.../video.mp4"
}
```

Também são aceitos os campos `video`, `url` ou `path`.

## 3. Agnes / provedores grátis por API

A ideia é criar um adaptador específico quando a API/documentação estiver definida.

Por enquanto, pode ser conectado pelo `cloud_webhook` caso exista um endpoint HTTP que receba prompt e retorne vídeo.

## 4. ComfyUI

Caminho planejado:

1. montar workflow visual no ComfyUI;
2. exportar workflow JSON;
3. enviar prompt/imagem via API local ou remota;
4. receber vídeo final no Video AI.

Futuro adaptador:

```txt
video_ai/providers/comfyui.py
```

## 5. SwarmUI / WanGP

Essas GUIs podem funcionar como camada de teste. O Video AI pode usar os melhores workflows delas como backend ou referência.

## Critérios para escolher provedores

- Tem camada grátis real?
- Tem fila aceitável?
- Retorna vídeo sem watermark?
- Permite uso comercial/institucional?
- Permite imagem de referência?
- Permite chamada por API?
- Permite controlar duração, resolução e seed?

## Prioridade inicial

1. Mock local para validar a interface.
2. Hugging Face Spaces públicos.
3. Cloud webhook genérico.
4. Adaptador específico para Agnes ou outro provedor grátis testado.
5. ComfyUI remoto/local.
