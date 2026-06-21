# RAG Chatbot — AWS Bedrock + FastAPI + Streamlit

A containerized **Retrieval-Augmented Generation (RAG)** chatbot built around **AWS Bedrock (Claude)**, with a **FastAPI** backend, a **Streamlit** frontend, a local **ChromaDB** vector store for context retrieval, and a CI/CD pipeline deploying to **AWS EC2**.

The system retrieves relevant context from a local knowledge base and augments the LLM prompt before generating a response, producing grounded, context-aware answers.

---

## Architecture

```
┌──────────────┐        HTTP         ┌──────────────────┐       ┌──────────────────┐
│  Streamlit   │  ───────────────▶   │   FastAPI         │ ────▶ │   AWS Bedrock     │
│  Frontend    │  /chat, /rag/chat   │   Backend         │       │   (Claude)        │
│  (chat UI)   │  ◀───────────────   │                   │ ◀──── │                   │
└──────────────┘     JSON / stream   └──────────────────┘       └──────────────────┘
                                              │
                                    retrieve top-k context
                                              ▼
                                     ┌──────────────────┐
                                     │  ChromaDB         │
                                     │  Vector Store     │
                                     └──────────────────┘
```

On a RAG request, the backend embeds the user query, retrieves the most relevant documents from ChromaDB, injects them as context into the prompt, and sends the augmented prompt to Claude via AWS Bedrock. Both services run as separate Docker containers, orchestrated with `docker-compose` over a shared bridge network.

---

## Tech Stack

| Layer            | Technology |
|------------------|------------|
| LLM              | AWS Bedrock — Claude (Sonnet) |
| Retrieval        | ChromaDB vector store |
| Backend          | FastAPI, Uvicorn, Pydantic |
| Frontend         | Streamlit |
| Containerization | Docker, docker-compose |
| CI/CD            | GitHub Actions |
| Deployment       | AWS EC2 |
| Code quality     | Black, isort, Ruff |

---

## Features

- **Retrieval-Augmented Generation** — retrieves relevant context from a ChromaDB knowledge base and grounds Claude's responses in it.
- **Conversational chat** with AWS Bedrock (Claude), including multi-turn conversation history.
- **Streaming responses** via a dedicated server-sent-events endpoint (`/chat/stream`).
- **Local knowledge base** powered by ChromaDB with semantic search over stored documents.
- **Streamlit chat interface** with conversation history, a RAG toggle, settings sidebar, backend health indicator, and response metadata.
- **Health & status endpoints** for monitoring (`/`, `/health`).
- **Fully containerized** backend and frontend, runnable with a single `docker-compose up`.
- **CI/CD pipeline** that validates dependencies and core imports on every push / pull request.

---

## Project Structure

```
.
├── main.py                      # FastAPI app & route definitions (incl. /rag/chat)
├── bedrock_service.py           # AWS Bedrock client (chat, streaming, RAG)
├── knowledge_base_service.py    # ChromaDB vector store service
├── models.py                    # Pydantic request/response schemas
├── config.py                    # Environment-based configuration
├── run_backend.py               # Local dev runner (uvicorn + reload)
├── frontend/
│   ├── app.py                   # Streamlit chat application
│   └── Dockerfile
├── backend/
│   └── Dockerfile
├── docker-compose.yml           # Orchestrates backend + frontend
├── requirements.txt
├── pyproject.toml               # Black / isort config
└── .github/workflows/deploy.yml # CI/CD pipeline
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- An AWS account with **Bedrock access** to the Claude model
- (Optional) Docker & docker-compose

### 1. Configure environment variables

Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
CLAUDE_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### 2. Run locally (without Docker)

```bash
pip install -r requirements.txt

# Terminal 1 — backend
python run_backend.py        # serves on http://127.0.0.1:8000

# Terminal 2 — frontend
streamlit run frontend/app.py
```

### 3. Run with Docker

```bash
docker-compose up --build
```

| Service   | URL                     |
|-----------|-------------------------|
| Frontend  | http://localhost:8502   |
| Backend   | http://localhost:8080   |

---

## API Endpoints

| Method | Endpoint                | Description |
|--------|-------------------------|-------------|
| `GET`  | `/`                     | Root health check |
| `GET`  | `/health`               | Detailed health check (model, region) |
| `POST` | `/chat`                 | Non-streaming chat completion |
| `POST` | `/rag/chat`             | RAG chat completion (retrieves context from the knowledge base) |
| `POST` | `/chat/stream`          | Streaming chat completion (SSE) |
| `GET`  | `/knowledge-base/info`  | Knowledge base collection info |
| `POST` | `/knowledge-base/search`| Semantic search over the knowledge base |
| `GET`  | `/conversations`        | Conversation history (placeholder) |

**Example RAG request:**

```bash
curl -X POST http://127.0.0.1:8000/rag/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is retrieval-augmented generation?", "conversation_history": []}'
```

---

## Deployment

The application is deployed to **AWS EC2** via a GitHub Actions workflow (`.github/workflows/deploy.yml`) that runs on pushes to `main` / `master`. The pipeline installs dependencies and validates that all core modules import correctly before deployment.

---

## Roadmap

- [ ] Add document ingestion (upload / chunk / embed) to populate the vector store from user files.
- [ ] Surface retrieved context and source citations in the Streamlit UI.
- [ ] Replace credentials-in-env with EC2 IAM roles for Bedrock access.
- [ ] Add unit/integration tests to the CI pipeline.

---

## License

Specify a license here (e.g. MIT) if you intend to share this publicly.
