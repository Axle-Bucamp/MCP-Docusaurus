# Stage 1: Build Docusaurus docs
FROM node:18-bullseye AS docusaurus-builder

WORKDIR /app/docs
COPY app/docs/ /app/docs/
RUN npm install && npm run build

# Stage 2: Build and run Python FastAPI app with uv
FROM python:3.11-slim AS fastapi-app

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && curl -Ls https://astral.sh/uv/install.sh | bash \
    && apt-get remove --purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Add ~/.cargo/bin to PATH for uv
ENV PATH="/root/.cargo/bin:$PATH"

# Copy Python dependencies
COPY requirements.txt pyproject.toml ./

# Install Python dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy Python application code
COPY app/ /app/app/

# Copy Docusaurus build output
COPY --from=docusaurus-builder /app/docs/build /app/docs/build

# Set environment variable for uv to avoid warning (optional)
ENV UV_CACHE_DIR="/app/.uv_cache"

# Expose FastAPI app port
EXPOSE 8000

# Run the app (make sure `main.py` exists inside /app and uses `if __name__ == "__main__"`)
CMD ["python", "main.py"]
