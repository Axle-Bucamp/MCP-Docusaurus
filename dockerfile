# Stage 1: Build Docusaurus static site
FROM node:18-bullseye AS docusaurus-builder

WORKDIR /app/docs
COPY app/docs/ /app/docs/
RUN npm install && npm run build

# Stage 2: Python FastAPI app with uv and fastmcp
FROM python:3.12-bullseye AS fastapi-app

# Use official UV binary for performance
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY app/ app/

# Install dependencies using uv
RUN uv pip install --system .

# Copy static Docusaurus site into final image
COPY --from=docusaurus-builder /app/docs/build /app/docs/build

# Set environment variables (optional: fallback defaults)
ENV FASTMCP_TRANSPORT=http
ENV FASTMCP_PORT=8000

# Expose FastAPI port
EXPOSE 8000

# Run the app via `fastmcp`
CMD ["fastmcp", "run", "main.py", "--transport", "http", "--port", "8000"]
