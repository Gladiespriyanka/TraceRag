from sqlalchemy import select
from packages.db.models import Chunk,Document
async def hydrate_candidates(db,candidates):
    if not candidates:return []
    ids=[x["chunk_id"] for x in candidates]
    r=await db.execute(select(Chunk,Document).join(Document,Chunk.document_id==Document.id).where(Chunk.id.in_(ids)))
    rows={c.id:(c,d) for c,d in r}; out=[]
    for x in candidates:
        if x["chunk_id"] not in rows:continue
        c,d=rows[x["chunk_id"]]; out.append({"chunk_id":c.id,"document_id":d.id,"filename":d.filename,"content":c.content,"metadata":d.metadata_json or {},"retrieval_score":x["score"]})
    return out
