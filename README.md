# 🧠 MCP Docusaurus Toolkit

A modular Content Management Platform (MCP) to manage, embed, and search Docusaurus documentation using **FastAPI**, self-hosted embeddings, and **PostgreSQL + pgvector**.

---

## 🚀 Features

- 📁 Auto-generate site map from Docusaurus docs
- 📝 Create, update, and continue editing Markdown docs
- 🧠 Vectorize content using pluggable embedding models
- 🔍 Perform RAG-style semantic search across the docs
- 🧾 Track incomplete docs with watermarks
- 🔄 Sync external edits into the vector database
- 🎨 Apply style/theme transformations to docs
- 🧪 Built-in tool decorators for AI agent control

---

## 📂 Project Structure

```

.
├── app/
│   ├── main.py             # FastAPI entrypoint with FastMCP + tools
│   ├── routes/             # Modular endpoints (docs, search, styles, site\_map)
│   ├── embeddings/         # Embedding model configuration + logic
│   ├── database.py         # PostgreSQL + pgvector connection logic
│   ├── models/             # DB + Pydantic models for documents
│   ├─── utils/              # Sync tools, helpers
│   └── docs/             # Full editable Docusaurus source (used in dev mode)
│
├── data/
│   ├── docusaurus/         # Runtime-synced Markdown docs
│   └── embeddings/         # Persisted vector embeddings
│
├── Dockerfile              # Multi-stage (Node + Python)
├── docker-compose.yml      # Services: FastAPI, Docusaurus Dev, Postgres
├── requirements.txt
└── README.md

````

---

## 🐳 Getting Started (Docker)

```bash
# 1. Clone this repository
git clone https://github.com/your-org/mcp-docusaurus.git
cd mcp-docusaurus

# 2. Launch services
docker compose up --build
````

* 🌐 MCP API available at: [http://localhost:8000](http://localhost:8000)
* 📚 Docusaurus live dev server: [http://localhost:3000](http://localhost:3000)

---

## 🧰 Tooling Overview (MCP API)

### ➕ Create a New Document

```http
POST /tool/create_document
```

```json
{
  "path": "guides/new-feature.md",
  "title": "New Feature",
  "content": "## Work in Progress..."
}
```

---

### ✍️ Update Existing Document

```http
POST /tool/update_docs
```

```json
{
  "path": "guides/new-feature.md",
  "line_begin": 10,
  "line_end": 15,
  "new_text": "Updated explanation here."
}
```

---

### 🧠 Vector Search (RAG-Style)

```http
POST /tool/search_docs
```

```json
{
  "query": "How to authenticate a plugin?"
}
```

---

### 🎨 Apply CSS or Theme Style

```http
POST /tool/apply_style
```

```json
{
  "style_id": "dark-theme",
  "content": "..."
}
```

---

## 🔌 Embedding Model Support

Pluggable embedding model backend with simple config.

### ✅ Local (Default)

* `sentence-transformers/all-MiniLM-L6-v2`

### 🌐 Optional Remote Support

* OpenAI Embeddings (requires API key)

---

## ⚙️ Environment Configuration

Use `.env` file or Docker `environment:` block:

```env
PG_HOST=postgres
PG_USER=postgres
PG_PASSWORD=postgres
PG_DATABASE=vector_db
EMBEDDING_MODEL=local
```

---

## 🔐 Security

* 🔒 Tool routes are gated with `@tool` decorators
* ✏️ Document writes are verified before embedding
* 🔑 Optional OAuth2 / API Token guardrails available

---

## 📘 Docusaurus Notes

* The `doc/` directory holds the full Docusaurus source (used for live editing).
* The `data/docusaurus/` directory contains generated Markdown synced with the vector database.

---

## 📊 Metrics & Health

* `GET /tool/health_check` – Check if the API is alive
* `GET /tool/metrics` – Prometheus/Grafana-compatible stats

---

## 📝 License

MIT License ©️ \[guidry company]



