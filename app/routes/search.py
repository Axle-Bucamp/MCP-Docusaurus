from fastapi import HTTPException
from app.embeddings.embeding import get_embedding
from app.models.vector_doc import search_embedding
import logging

logger = logging.getLogger(__name__)

def perform(query: str, top_k: int = 5, min_score: float = 0.0) -> dict:
    """
    Performs semantic search over embedded documents using vector similarity.

    Args:
        query (str): The input search query string.
        top_k (int): Maximum number of top matching documents to return.
        min_score (float): Minimum similarity score threshold for results.

    Returns:
        dict: Dictionary containing the original query and a list of matched results,
              each with path, score, and content snippet.
    """
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Search query must not be empty.")

    try:
        embedding = get_embedding(query)
    except Exception as e:
        logger.exception("Embedding generation failed.")
        raise HTTPException(status_code=500, detail="Failed to generate query embedding.")

    if not embedding:
        raise HTTPException(status_code=500, detail="Generated embedding is empty.")

    try:
        matches = search_embedding(embedding=embedding, top_k=top_k)
    except Exception as e:
        logger.exception("Vector search failed.")
        raise HTTPException(status_code=500, detail="Vector search failed.")

    filtered_results = [
        {
            "path": match.path,
            "score": round(match.score, 4),
            "snippet": match.content[:300].strip()
        }
        for match in matches if match.score >= min_score
    ]

    return {
        "query": query,
        "results": filtered_results
    }
