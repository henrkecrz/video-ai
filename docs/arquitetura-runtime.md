# Arquitetura runtime do Video AI

Esta etapa incorporou as principais ideias analisadas no projeto Free Claude Code, adaptadas para geração de vídeo.

## Fluxo atual

```txt
app.py
↓
main.py
↓
video_ai.runtime
↓
ProviderRegistry
↓
ProviderCatalog
↓
Provider concreto
```

## Arquivos adicionados

- `video_ai/provider_catalog.py`: catálogo central dos provedores, capacidades e status de implementação.
- `video_ai/providers/runtime_registry.py`: registry runtime com cache e lazy loading.
- `video_ai/admin_config.py`: manifesto de configuração e utilitários para salvar/carregar `.env`.
- `video_ai/runtime.py`: fachada simples para a interface chamar geração, listar provedores e limpar cache.
- `main.py`: nova interface Gradio com abas.

## Abas da interface

### Gerar vídeo

Mantém o fluxo original: prompt, prompt negativo, imagem opcional, resolução, duração, seed e provedor.

### Provedores

Permite configurar Hugging Face Space, webhook cloud e campos reservados para Agnes/ComfyUI sem editar código.

### Diagnóstico

Mostra uma tabela com catálogo de provedores, implementação, tipo de transporte, capacidades, credencial e endpoint.

## Provedores implementados

- `mock`: teste local sem chamada externa.
- `huggingface_space`: Spaces compatíveis com `gradio_client`.
- `cloud_webhook`: endpoint HTTP genérico que retorna vídeo.

## Provedores planejados

- `agnes`;
- `comfyui`;
- `colab_kaggle`;
- `replicate_fal`.

## Decisão importante

O projeto passa a separar melhor:

```txt
Interface → Runtime → Registry → Catalog → Provider
```

Isso prepara o Video AI para receber novos modelos sem transformar a interface em um bloco de condicionais.
