import os
from pathlib import Path
from typing import List

from fastapi import HTTPException
from app.embeddings.embeding import get_embedding
from app.models.vector_doc import upsert_embedding, delete_embedding

DOCS_DIR = Path("/app/docs")
WATERMARK = "<!-- TODO: INCOMPLETE -->"


def create_document(path: str, content: str, mark_incomplete: bool = True) -> dict:
    """Creates a new markdown file, optionally adds watermark, and stores embedding."""
    full_path = DOCS_DIR / path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    if mark_incomplete and WATERMARK not in content:
        content += f"\n\n{WATERMARK}"

    full_path.write_text(content)
    vector = get_embedding(content)

    upsert_embedding(path=str(path), embedding=vector, content=content)
    return {"status": "created", "path": path}


def update_document(path: str, start_line: int, end_line: int, new_text: str) -> dict:
    """Updates lines in a document and re-generates the embedding."""
    full_path = DOCS_DIR / path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    lines = full_path.read_text().splitlines()
    lines[start_line:end_line] = new_text.splitlines()
    updated = "\n".join(lines)

    full_path.write_text(updated)
    vector = get_embedding(updated)
    upsert_embedding(path=path, embedding=vector, content=updated)
    return {"status": "updated", "path": path}


def continue_document(path: str, continuation: str) -> dict:
    """Appends content and removes watermark if document is complete."""
    full_path = DOCS_DIR / path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    current = full_path.read_text()
    updated = current.strip() + "\n" + continuation
    if WATERMARK in updated and not continuation.strip().endswith(WATERMARK):
        updated = updated.replace(WATERMARK, "")

    full_path.write_text(updated)
    vector = get_embedding(updated)
    upsert_embedding(path=path, embedding=vector, content=updated)
    return {"status": "continued", "path": path}


def get_unfinished_documents() -> List[str]:
    """Scans all documents and returns paths with watermark present."""
    unfinished = []
    for file in DOCS_DIR.rglob("*.md"):
        content = file.read_text()
        if WATERMARK in content:
            unfinished.append(str(file.relative_to(DOCS_DIR)))
    return unfinished


def delete_document(path: str) -> dict:
    """Deletes markdown file and removes associated embedding."""
    full_path = DOCS_DIR / path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    full_path.unlink()
    delete_embedding(path)
    return {"status": "deleted", "path": path}


def get_content(path: str) -> str:
    """Returns full markdown content of a given document."""
    full_path = DOCS_DIR / path
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")

    return full_path.read_text()