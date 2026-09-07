from functools import lru_cache
from sentence_transformers import SentenceTransformer
from packages.core.config import settings
class EmbeddingProvider:
    def __init__(self,model_name=None):
        self.model=SentenceTransformer(model_name or settings.embedding_model,device=settings.embedding_device)
    def embed(self,texts):
        if not texts:return []
        return self.model.encode(texts,normalize_embeddings=True,show_progress_bar=False).tolist()
@lru_cache
def get_embedder():return EmbeddingProvider()
