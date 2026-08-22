# Agente Jurídico (CrewAI)

Agente de IA para análise de questões jurídicas brasileiras, construído com
[CrewAI](https://www.crewai.com/) e exposto via API [FastAPI](https://fastapi.tiangolo.com/).

O time é composto por dois agentes que trabalham em sequência:

1. **Pesquisador Jurídico** — pesquisa informações sobre o tema usando a
   ferramenta [Serper](https://serper.dev/) (busca no Google), priorizando
   fontes oficiais (legislação, tribunais, órgãos reguladores, Planalto etc.).
2. **Assistente Jurídico** — usa exclusivamente o resultado da pesquisa para
   produzir uma análise clara e fundamentada, com as fontes consultadas.

```
Pergunta do usuário
        │
        ▼
Pesquisador Jurídico (LLM + Serper) ── resumo com fontes
        │
        ▼
Assistente Jurídico (LLM) ── resposta estruturada (Resposta / Fundamentos / Fontes)
```

## Estrutura do projeto

```
ai_agent_juridico/
├── app/
│   ├── api.py          # API FastAPI (endpoints)
│   └── crew.py         # Definição dos agentes, tasks e crew (CrewAI)
├── scripts/
│   ├── cli.py           # Executa o agente via terminal, sem precisar da API
│   ├── cliente_api.py   # Cliente HTTP de exemplo para testar a API
│   ├── teste_llm.py     # Script manual para testar a chamada ao LLM
│   └── teste_serper.py  # Script manual para testar a busca via Serper
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Pré-requisitos

- Python 3.13+
- Uma chave de API da [OpenAI](https://platform.openai.com/) (`OPENAI_API_KEY`)
- Uma chave de API do [Serper](https://serper.dev/) (`SERPER_API_KEY`)
- Docker + Docker Compose (opcional, para rodar em container)

## Configuração

Copie o arquivo de exemplo e preencha suas chaves:

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=sua-chave-openai
SERPER_API_KEY=sua-chave-serper
```

## Como rodar

### Localmente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.api:app --reload
```

A API sobe em `http://127.0.0.1:8000`.

### Via Docker

```bash
docker compose up --build
```

## Usando a API

**Verificar status:**

```bash
curl http://127.0.0.1:8000/
```

**Fazer uma pergunta jurídica:**

```bash
curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Quais são os direitos do consumidor em compras online?"}'
```

Resposta:

```json
{
  "pergunta": "Quais são os direitos do consumidor em compras online?",
  "resposta": "## Resposta\n...\n## Fundamentos\n...\n## Fontes consultadas\n..."
}
```

### Endpoints

| Método | Rota       | Descrição                                    |
|--------|------------|-----------------------------------------------|
| GET    | `/`        | Health check (`{"status": "online"}`)         |
| POST   | `/execute` | Executa o time de agentes para uma `pergunta` |

## Scripts utilitários

Com a API rodando em outro terminal, é possível testar o cliente de exemplo:

```bash
python -m scripts.cliente_api
```

Ou rodar o agente diretamente pelo terminal, sem precisar da API:

```bash
python -m scripts.cli
```
