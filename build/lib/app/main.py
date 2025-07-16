from app.routes import document, search, site_map, style
from fastmcp import FastMCP
from fastmcp.decorators import tool
import utils

app = FastMCP()

@tool(name="health_check", description="Check if the service is up")
async def health_check() -> dict:
    """Health check endpoint to verify service status."""
    return {"status": "ok", "service": "mcp-docusaurus"}

@tool(name="metrics", description="Return metrics for the service")
async def metrics() -> dict:
    """Return service metrics in Grafana/Prometheus-compatible format."""
    return {
        "uptime": "TODO",
        "total_requests": 0,
        "active_sessions": 0
    }

@tool(name="create_document", description="Create a new documentation entry")
async def create_document(path: str, title: str, content: str) -> dict:
    """Creates a new markdown doc, embeds content, stores metadata."""
    return document.create_document(path, f"# {title}\n\n{content}")

@tool(name="update_docs", description="Update a document at the given position")
async def update_docs(path: str, line_begin: int, line_end: int, new_text: str) -> dict:
    """Updates lines between given range in an existing document."""
    return document.update_document(path, line_begin, line_end, new_text)

@tool(name="continue_docs", description="Continue writing the document at end")
async def continue_docs(path: str, continuation: str) -> dict:
    """Appends content to the document, and removes TODO watermark if complete."""
    return document.continue_document(path, continuation)

@tool(name="get_docs", description="Get the content of a document at a given path")
async def get_docs(path: str) -> dict:
    """Returns markdown content of a document by path."""
    return {"path": path, "content": document.get_content(path)}

@tool(name="unfinished_docs", description="Get all the unfinished documents")
async def unfinished_docs() -> dict:
    """Lists all documents still marked with <!-- TODO: INCOMPLETE -->."""
    return {"unfinished": document.get_unfinished_documents()}

@tool(name="search_docs", description="Search knowledge in documentation embeddings")
async def search_docs(query: str) -> dict:
    """Performs semantic vector search across embedded documents."""
    utils.resync_if_external_changes()
    
    return search.perform_search(query)

@tool(name="get_sitemap", description="Retrieve sitemap")
async def get_sitemap() -> dict:
    """Generates a tree view of documentation files and structure."""
    return site_map.generate_sitemap()

@tool(name="apply_style", description="Apply style transformation to a document")
async def apply_style(style_id: str, content: str) -> dict:
    """Transforms markdown/CSS style of given content based on style ID."""
    return style.apply_style(style_id, content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
