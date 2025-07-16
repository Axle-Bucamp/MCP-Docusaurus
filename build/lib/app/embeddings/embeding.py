from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from typing import Literal
import os

class EmbeddingConfig(BaseModel):
    provider: Literal["instructor", "huggingface", "openai"] = Field("instructor", description="Embedding model backend")
    model_name: str = Field("hkunlp/instructor-xl", description="Model path or name")
    device: str = Field("cpu", description="Device to use: 'cpu' or 'cuda'")

# Default config from env or fallback
config = EmbeddingConfig(
    provider=os.getenv("EMBEDDING_PROVIDER", "instructor"),
    model_name=os.getenv("EMBEDDING_MODEL", "hkunlp/instructor-xl"),
    device=os.getenv("EMBEDDING_DEVICE", "cpu")
)

# Global model instance
embedding_model = None

def load_embedding_model():
    global embedding_model
    if config.provider in ["instructor", "huggingface"]:
        embedding_model = SentenceTransformer(config.model_name, device=config.device)
    elif config.provider == "openai":
        # Placeholder: OpenAI usage would require `openai` and API key
        raise NotImplementedError("OpenAI embedding support is not implemented in local mode.")
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


def get_embedding(text: str) -> list[float]:
    if embedding_model is None:
        load_embedding_model()
    return embedding_model.encode(text).tolist()
