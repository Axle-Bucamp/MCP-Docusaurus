import json
from pathlib import Path
from fastapi import HTTPException
from app.routes.site_map import generate
from app.embeddings.embeding import get_embedding
from app.models.vector_doc import upsert_embedding

SITEMAP_SNAPSHOT = Path("/app/.mcp_last_sitemap.json")
DOCS_DIR = Path("/app/docs")


def load_last_snapshot():
    if SITEMAP_SNAPSHOT.exists():
        with SITEMAP_SNAPSHOT.open("r") as f:
            return json.load(f)
    return {}


def save_snapshot(sitemap):
    with SITEMAP_SNAPSHOT.open("w") as f:
        json.dump(sitemap, f, indent=2)


def flatten_sitemap(sitemap, prefix=""):
    result = []
    for node in sitemap:
        if isinstance(node, dict):
            for key, val in node.items():
                result.extend(flatten_sitemap(val, prefix + key + "/"))
        else:
            result.append(prefix + node)
    return result


def resync_if_external_changes():
    """
    Compare the current sitemap with the last saved snapshot. If any new docs were
    added outside MCP (e.g., manually by humans), embed them before continuing.
    """
    current_sitemap = generate()
    current_flat = set(flatten_sitemap(current_sitemap))

    last_snapshot = load_last_snapshot()
    last_flat = set(flatten_sitemap(last_snapshot))

    new_files = current_flat - last_flat

    for relative_path in new_files:
        full_path = DOCS_DIR / relative_path
        if full_path.exists():
            content = full_path.read_text()
            vector = get_embedding(content)
            upsert_embedding(path=relative_path, embedding=vector, content=content)
        else:
            raise HTTPException(status_code=404, detail=f"Missing file in docs: {relative_path}")

    # Update the snapshot
    save_snapshot(current_sitemap)
    return {"synced": True, "new_files_indexed": list(new_files)}