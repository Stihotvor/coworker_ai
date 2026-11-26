# CoworkerAI — Agent Instructions & Project Context

## Project Overview
**CoworkerAI** is an AI assistant designed to help team members navigate company documentation and Jira tickets using Retrieval-Augmented Generation (RAG). It provides accurate answers regarding tasks, bugs, project statuses, and company processes.

---

## Architecture & Tech Stack
- **Language & Runtime**: Python 3.12
- **RAG & Agent Framework**: [LlamaIndex](https://www.llamaindex.ai/) (`llama-index`, `llama-index-vector-stores-chroma`, `llama-index-llms-lmstudio`, `llama-index-storage-kvstore-redis`, `llama-index-retrievers-bm25`)
- **LLM & Embeddings Backend**: LMStudio (Mistral 7B Instruct and `all-MiniLM-L6-v2`) exposed via OpenAI-compatible endpoints on host (`http://host.docker.internal:1234/v1` or `http://localhost:1234/v1`)
- **Vector Database**: ChromaDB (stores text chunks categorized by document type: `tickets` and `documentation`)
- **Caching & Session Storage**: Redis (KV store for ingestion pipeline cache and chat history per session)
- **Web API & UI**:
  - **FastAPI**: Backend REST service providing health checks (`/healthcheck/`, `/healthcheck-redis/`)
  - **Gradio**: Interactive web chat interface mounted to FastAPI at the root (`src.ui.entrypoints.mounted_app`)

---

## Directory Structure & Responsibilities
- `src/settings.py`: Central configuration initializing LlamaIndex `Settings` (LLM client, custom LMStudio embeddings, semantic text splitter).
- `src/ui/`:
  - `main.py`: Gradio interface setup (Chatbot, Related Tasks, Related Documents, Reindex button).
  - `datastructures.py`: Data models for `Task`, `Document`, `RelatedTasks`, and `RelatedDocuments`.
  - `entrypoints/`: Entrypoints for running Gradio standalone or mounted with FastAPI.
- `src/api/`:
  - `main.py`: FastAPI application routing, settings initialization, and health checks.
- `src/role/`:
  - `chat_manager.py`: Core coordination layer (`ChatManager`) bridging UI and RAG engine. Manages query prediction, response streaming, chat history, and retrieval of related tasks/documents.
  - `llm_client.py`: Client wrapper for LMStudio completions and streaming chat.
  - `prompt_repository/`: Prompt templates (system prompt: `coworker.md`).
- `src/storage/`:
  - `vector_db.py`: `VectorStoreIndexManager` managing ChromaDB collection and chat engine setup.
  - `data_ingestion.py`: `DataIngestionManager` handling document parsing and caching via Redis.
  - `chat_repository.py`: Redis-backed storage for session chat history.
  - `custom_transformations.py`: Node transformations (e.g. `TextCleaner`, `DocumentTypeToMetadata`).
  - `custom_embedding_clients/`: `LMStudioEmbedding` class implementing LlamaIndex `BaseEmbedding`.
- `data/`:
  - `tickets/`: Plain text files containing Jira ticket data (one ticket per file).
  - `documentation/`: Plain text files containing company documentation (one document per file).
- `tests/`: Unit and integration test suites.

---

## Local Development & Service Orchestration
The project uses `docker-compose.yml` to orchestrate services:
- **`coworker-ai`**: FastAPI + Gradio server on port `8010`.
- **`chromadb`**: Vector store service on port `8000` (internal network `coworker-net`).
- **`redis`**: Cache and session store on port `6379`.
- **LMStudio**: Must be running on the host machine listening on port `1234`.

### Useful Commands
- **Start containers**:
  ```bash
  docker-compose up
  ```
- **Access UI**:
  Open `http://localhost:8010` in the browser.

---

## Testing Guidelines
- **Unit Tests**:
  ```bash
  poetry run pytest -m unit
  ```
- **Integration Tests**:
  ```bash
  poetry run pytest -m integration
  ```
- All new features and bug fixes should include corresponding tests in `tests/`.
