# Video AI

Interface simples para gerar vídeos com IA usando provedores em nuvem e modelos gratuitos/abertos.

A ideia do projeto é funcionar como um **painel GUI** para testar e combinar diferentes fontes de geração de vídeo, começando por:

- Hugging Face Spaces públicos, incluindo Spaces com ZeroGPU quando disponíveis;
- provedores gratuitos ou com camada grátis configuráveis por API;
- provedores pagos opcionais, como fallback futuro;
- workflows locais/externos, como ComfyUI, SwarmUI ou WanGP.

> Status: MVP inicial. A base já vem com uma interface Gradio, sistema de provedores plugáveis e configuração por `.env`.

## Objetivo

Criar uma ferramenta prática para:

1. escrever um prompt;
2. escolher um provedor/modelo;
3. enviar a geração para nuvem quando disponível;
4. receber o vídeo final;
5. futuramente salvar histórico, presets e workflows.

## Estrutura inicial

```txt
video-ai/
├── app.py
├── requirements.txt
├── .env.example
├── video_ai/
│   ├── config.py
│   ├── orchestrator.py
│   └── providers/
│       ├── base.py
│       ├── mock.py
│       ├── huggingface_space.py
│       └── cloud_webhook.py
└── docs/
    └── provedores.md
```

## Como rodar localmente

```bash
git clone https://github.com/henrkecrz/video-ai.git
cd video-ai
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Depois, abra o endereço mostrado no terminal, geralmente:

```txt
http://127.0.0.1:7860
```

## Configuração rápida

No arquivo `.env`, configure o provedor que deseja usar.

### Modo teste, sem API

```env
DEFAULT_PROVIDER=mock
```

Esse modo apenas valida a interface e o fluxo interno.

### Hugging Face Space

```env
DEFAULT_PROVIDER=huggingface_space
HF_SPACE_ID=usuario/space-name
HF_API_NAME=/predict
HF_TOKEN=
```

O `HF_TOKEN` é opcional para Spaces públicos, mas pode ser necessário para alguns Spaces privados ou com autenticação.

### Provedor cloud genérico

```env
DEFAULT_PROVIDER=cloud_webhook
CLOUD_WEBHOOK_URL=https://exemplo.com/api/generate
CLOUD_WEBHOOK_KEY=sua-chave
```

Esse adaptador serve para APIs gratuitas ou webhooks que aceitem prompt e retornem uma URL de vídeo.

## Próximos passos planejados

- [ ] adicionar histórico de gerações;
- [ ] criar presets para vídeos institucionais, reels e cards animados;
- [ ] adicionar suporte a imagem de referência;
- [ ] adicionar fila de geração;
- [ ] integrar workflows do ComfyUI via API;
- [ ] criar biblioteca de modelos/provedores gratuitos testados;
- [ ] empacotar em Docker;
- [ ] preparar deploy no Hugging Face Spaces.

## Observação sobre provedores grátis

Provedores gratuitos podem ter fila, limite diário, instabilidade ou mudanças de política. O projeto foi estruturado para trocar provedores sem reescrever a interface.
