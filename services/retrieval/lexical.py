from sqlalchemy import text


async def lexical_search(
    db,
    query,
    top_k=50,
    metadata=None,
    document_id=None,
):
    sql = """
        SELECT
            id,
            ts_rank_cd(
                to_tsvector('english', content),
                websearch_to_tsquery('english', :query)
            ) AS score
        FROM chunks
        WHERE to_tsvector('english', content)
              @@ websearch_to_tsquery('english', :query)
    """

    params = {
        "query": query,
        "top_k": top_k,
    }

    if document_id is not None:
        sql += """
            AND document_id = :document_id
        """
        params["document_id"] = document_id

    sql += """
        ORDER BY score DESC
        LIMIT :top_k
    """

    result = await db.execute(
        text(sql),
        params,
    )

    return [
        {
            "chunk_id": row.id,
            "score": float(row.score),
        }
        for row in result
    ]