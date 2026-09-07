from sentence_transformers import CrossEncoder
from packages.core.config import settings
class NLIEngine:
    def __init__(self):self.model=CrossEncoder("cross-encoder/nli-deberta-v3-base",device=settings.reranker_device)
    def compare(self,premise,hypothesis):
        x=self.model.predict([(premise,hypothesis)])[0]
        return {"raw_scores":x.tolist() if hasattr(x,"tolist") else float(x)}
