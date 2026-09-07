from services.ingestion.embedder import get_embedder
from services.retrieval.lexical import lexical_search
from services.retrieval.vector import vector_search
from services.retrieval.rrf import reciprocal_rank_fusion
from services.retrieval.candidates import hydrate_candidates
from services.reranking.cross_encoder import CrossEncoderReranker


class RetrievalEngine:

    def __init__(self):
        self.reranker = CrossEncoderReranker()

    async def retrieve(
        self,
        db,
        query,
        retrieval_k=50,
        top_k=5,
        document_id=None,
    ):

        # Generate query embedding
        e = get_embedder().embed([query])[0]

        # Lexical + vector retrieval
        lexical_results = await lexical_search(
            db,
            query,
            retrieval_k,
            document_id=document_id,
        )

        vector_results = await vector_search(
            db,
            e,
            retrieval_k,
            document_id=document_id,
        )

        # Fuse both rankings
        fused = reciprocal_rank_fusion(
            [
                lexical_results,
                vector_results,
            ]
        )

        # Hydrate chunks/documents
        candidates = await hydrate_candidates(
            db,
            fused[:retrieval_k],
        )

        # Cross-encoder reranking
        return self.reranker.rerank(
            query,
            candidates,
            top_k,
        )