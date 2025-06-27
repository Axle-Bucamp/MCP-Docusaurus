# 🧠 MCP Docusaurus Toolkit

A modular Content Management Platform (MCP) to manage, embed, and search Docusaurus documentation using FastAPI, self-hosted embeddings, and PostgreSQL + `pgvector`.

---

## 🚀 Features

* 📁 Auto-generate site map from Docusaurus docs
* 📝 Create, update, and continue editing Markdown docs
* 🧠 Vectorize content using pluggable embedding models
* 🔍 Perform RAG-style search across the docs
* 🧾 Track incomplete docs with watermarks
* 🧹 Sync external edits into the vector database
* 🎨 Apply style transformations to docs (CSS/theme)
* 🧪 Built-in tool decorators for AI agent control

---

## 📂 Project Structure

```
.
├── app/
│   ├── main.py             # Entry point with FastMCP + tool decorators
│   ├── routes/             # Modular routes (document, search, style, site_map)
│   ├── embeddings/         # Embedding models and config
│   ├── database.py         # Postgres/pgvector connection
│   ├── models/             # Pydantic models and DB helpers
│   └── utils/              # Sync and helper tools
│
├── doc/                    # Full Docusaurus project (editable by devs)
├── data/
│   ├── docusaurus/         # Runtime-mounted editable docs
│   └── embeddings/         # Stored vectors and metadata
│
├── Dockerfile              # Multi-stage (Python + Node for Docusaurus)
├── docker-compose.yml      # Services: FastAPI, Docusaurus Dev, Postgres
├── requirements.txt
└── README.md
```

---

## 🐳 Getting Started (Docker)

```bash
# 1. Clone this repository
git clone https://github.com/your-org/mcp-docusaurus.git
cd mcp-docusaurus

# 2. Launch services
docker compose up --build
```

* MCP API available at: [http://localhost:8000](http://localhost:8000)
* Docusaurus live dev: [http://localhost:3000](http://localhost:3000)

---

## 🔧 Tooling Overview

### ➕ Create Document

```json
POST /tool/create_document
{
  "path": "guides/new-feature.md",
  "title": "New Feature",
  "content": "## Work in Progress..."
}
```

### ✍️ Update Document

Update lines in an existing doc:

```json
POST /tool/update_docs
{
  "path": "guides/new-feature.md",
  "line_begin": 10,
  "line_end": 15,
  "new_text": "Updated explanation here."
}
```

### 🧩 Vector Search (RAG)

```json
POST /tool/search_docs
{
  "query": "How to authenticate a plugin?"
}
```

### 🎨 Apply CSS Style

```json
POST /tool/apply_style
{
  "style_id": "dark-theme",
  "content": "..."
}
```

---

## 📦 Embedding Support

Supports any local or remote embedding models via Pydantic configuration.

### Local (default)

* Sentence Transformers (`all-MiniLM-L6-v2`)
* OpenAI (optional)

---

## 🛠 Env Configuration

Define `.env` or use Docker `environment:` block:

```env
PG_HOST=postgres
PG_USER=postgres
PG_PASSWORD=postgres
PG_DATABASE=vector_db
EMBEDDING_MODEL=local
```

---

## 🔐 Security

* Tool endpoints are isolated via decorators (`@tool`)
* External writes are verified before embedding
* Optional OAuth2/API token integration available

---

## 📘 Docusaurus Notes

The `doc/` directory contains the full Docusaurus project.
The `data/docusaurus/` directory holds generated Markdown docs that are synced with embeddings and updated via MCP.

---

## 📈 Metrics & Health

* `GET /tool/health_check`
* `GET /tool/metrics` *(prometheus/grafana format)*

---

## 📄 License

MIT License ©️ YourOrg

