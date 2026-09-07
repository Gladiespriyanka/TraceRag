from sqlalchemy import select

from packages.db.models import Chunk


async def vector_search(
    db,
    embedding,
    top_k=50,
    document_id=None,
):
    distance = Chunk.embedding.cosine_distance(embedding)

    query = (
        select(
            Chunk.id,
            (1 - distance).label("score"),
        )
        .where(
            Chunk.embedding.is_not(None)
        )
    )

    if document_id is not None:
        query = query.where(
            Chunk.document_id == document_id
        )

    query = (
        query
        .order_by(distance)
        .limit(top_k)
    )

    result = await db.execute(query)

    return [
        {
            "chunk_id": row.id,
            "score": float(row.score),
        }
        for row in result
    ]