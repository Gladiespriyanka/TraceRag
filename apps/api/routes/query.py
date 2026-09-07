import re

from fastapi import APIRouter, Depends
from sqlalchemy import select, func

from packages.core.config import settings
from packages.db.models import Document
from packages.db.session import get_db

from services.retrieval.engine import RetrievalEngine
from services.intelligence.decomposer import QueryDecomposer
from services.generation.answer import AnswerGenerator
from services.generation.confidence import confidence_score

from apps.api.schemas.query import QueryRequest, QueryResponse, QueryResult


router = APIRouter(prefix="/query", tags=["Query"])
engine = RetrievalEngine()


def extract_filename(query: str):
    """
    Detect a PDF filename mentioned in the query.
    """

    match = re.search(
        r'([A-Za-z0-9_-]+\.pdf)',
        query,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


@router.post("", response_model=QueryResponse)
async def query(req: QueryRequest, db=Depends(get_db)):

    # ---------------------------------------------------------
    # 1. Detect explicit document mentioned by the user
    # ---------------------------------------------------------

    requested_filename = extract_filename(req.query)

    document_id = None

    if requested_filename:

        document = await db.scalar(
            select(Document).where(
                func.lower(Document.filename)
                == requested_filename.lower()
            )
        )

        if document:
            document_id = document.id

            print(
                f"Document filter activated: "
                f"{document.filename} ({document.id})"
            )

        else:
            print(
                f"Document mentioned in query was not found: "
                f"{requested_filename}"
            )

    else:
        print("No explicit document mentioned in query.")

    # ---------------------------------------------------------
    # 2. Query decomposition
    # ---------------------------------------------------------

    subs = await QueryDecomposer().decompose(req.query)

    # ---------------------------------------------------------
    # 3. Hybrid retrieval
    # ---------------------------------------------------------

    results = []
    seen = set()

    for q in subs:

        retrieved = await engine.retrieve(
            db,
            q,
            50,
            req.top_k,
            document_id=document_id,
        )

        for r in retrieved:

            if r["chunk_id"] not in seen:
                seen.add(r["chunk_id"])
                results.append(r)

    results = results[:req.top_k]

    # ---------------------------------------------------------
    # 4. Answer generation
    # ---------------------------------------------------------

    answer = None
    citations = []
    conf = 0.0

    if results and settings.gemini_api_key:

        try:

            g = await AnswerGenerator().answer(
                req.query,
                results
            )

            answer = g.get("answer")
            citations = g.get("citations", [])

            conf = confidence_score(
                results,
                min(
                    1,
                    len(citations)
                    / max(
                        1,
                        len((answer or "").split("."))
                    )
                )
            )

        except Exception as exc:

            print(f"Answer generation failed: {exc}")

            answer = (
                "The evidence retrieval stage completed successfully, "
                "but the answer generation service is currently unavailable. "
                "Please check the Gemini API configuration/access."
            )

            citations = []
            conf = 0.0

    # ---------------------------------------------------------
    # 5. Build source objects
    # ---------------------------------------------------------

    sources = [
        QueryResult(
            chunk_id=str(r["chunk_id"]),
            document_id=str(r["document_id"]),
            filename=r["filename"],
            content=r["content"],
            retrieval_score=r["retrieval_score"],
            rerank_score=r["rerank_score"],
        )
        for r in results
    ]

    # ---------------------------------------------------------
    # 6. Return response
    # ---------------------------------------------------------

    return QueryResponse(
        query=req.query,
        answer=answer,
        confidence=conf,
        citations=citations,
        sources=sources,
        sub_queries=subs,
    )