# Base Python image for FastAPI
FROM node:18-bullseye as docusaurus-builder

# Build Docusaurus site
WORKDIR /app/doc
COPY doc/ /app/doc
RUN npm install && npm run build

# Now build the Python server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Copy Docusaurus build from previous stage
COPY --from=docusaurus-builder /app/doc /app/doc

# Expose port (optional, depending on how you run the server)
EXPOSE 8000

# Start FastAPI
CMD ["python", "app/main.py"]