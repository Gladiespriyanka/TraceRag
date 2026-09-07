from packages.db.models import Document,Chunk
from services.ingestion.parser import parse_bytes
from services.ingestion.chunker import chunk_text
from services.ingestion.embedder import get_embedder
async def ingest_document(db,data,filename,content_type):
    pieces=chunk_text(parse_bytes(data,content_type,filename))
    if not pieces:raise ValueError("No extractable text found")
    vectors=get_embedder().embed(pieces); doc=Document(filename=filename,content_type=content_type,size_bytes=len(data)); db.add(doc); await db.flush()
    for i,(content,vector) in enumerate(zip(pieces,vectors)):db.add(Chunk(document_id=doc.id,chunk_index=i,content=content,embedding=vector))
    await db.commit(); await db.refresh(doc); return doc
