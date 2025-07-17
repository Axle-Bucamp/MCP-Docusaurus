# Stage 1: Build Docusaurus static site
FROM node:18-bullseye AS docusaurus-builder

WORKDIR /app/docs
COPY app/docs/ /app/docs/
RUN npm install && npm run build

# Stage 2: Python FastAPI app with uv
FROM python:3.12-bullseye AS fastapi-app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

# Copy project files (exclude `data/`, `.git/`, etc.)
COPY pyproject.toml ./
COPY app/ app/

# Install Python dependencies
RUN uv pip install --system .

# Copy Docusaurus build output
COPY --from=docusaurus-builder /app/docs/build /app/docs/build

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI entrypoint
CMD ["uv", "run", "fastmcp", "run", "main.py"]
