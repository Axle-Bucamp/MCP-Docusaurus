from typing import List
from pydantic import BaseModel
from sqlalchemy import text
from app.database import get_db

class MatchResult(BaseModel):
    path: str
    score: float
    content: str

def upsert_embedding(path: str, embedding: List[float], content: str):
    """
    Insert or update a document embedding in PostgreSQL with pgvector.
    """
    db = get_db()
    db.execute(
        text("""
            INSERT INTO documents (path, embedding, content)
            VALUES (:path, :embedding, :content)
            ON CONFLICT (path) DO UPDATE
            SET embedding = EXCLUDED.embedding,
                content = EXCLUDED.content
        """),
        {"path": path, "embedding": embedding, "content": content}
    )
    db.commit()


def delete_embedding(path: str):
    """
    Delete an embedding entry by path.
    """
    db = get_db()
    db.execute(text("DELETE FROM documents WHERE path = :path"), {"path": path})
    db.commit()


def search_embedding(embedding: List[float], top_k: int = 5) -> List[MatchResult]:
    """
    Search the document store using pgvector for similar embeddings.
    """
    db = get_db()
    result = db.execute(
        text("""
            SELECT path, content,
                   1 - (embedding <#> :embedding) AS score
            FROM documents
            ORDER BY embedding <#> :embedding ASC
            LIMIT :top_k
        """),
        {"embedding": embedding, "top_k": top_k}
    )

    return [
        MatchResult(path=row["path"], score=row["score"], content=row["content"])
        for row in result.fetchall()
    ]