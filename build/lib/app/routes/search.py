from fastapi import HTTPException
from app.embeddings.embeding import get_embedding
from app.models.vector_doc import search_embedding


def perform(query: str, top_k: int = 5) -> dict:
    """
    Search for relevant documentation content using vector similarity.
    
    Args:
        query (str): The input search query.
        top_k (int): Number of top documents to retrieve.

    Returns:
        dict: List of top matches with path, score, and content snippet.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query string is required")

    embedding = get_embedding(query)
    matches = search_embedding(embedding=embedding, top_k=top_k)

    return {
        "query": query,
        "results": [
            {
                "path": match.path,
                "score": match.score,
                "snippet": match.content[:300]  # Preview the beginning of the content
            }
            for match in matches
        ]
    }