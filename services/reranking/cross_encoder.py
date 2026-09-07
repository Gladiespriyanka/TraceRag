from sentence_transformers import CrossEncoder
from packages.core.config import settings
class CrossEncoderReranker:
    def __init__(self):self.model=CrossEncoder(settings.reranker_model,device=settings.reranker_device)
    def rerank(self,query,candidates,top_k=5):
        if not candidates:return []
        scores=self.model.predict([(query,c["content"]) for c in candidates])
        return [{**c,"rerank_score":float(s)} for c,s in sorted(zip(candidates,scores),key=lambda x:float(x[1]),reverse=True)[:top_k]]
