from fastapi import APIRouter,Depends,File,UploadFile,HTTPException
from sqlalchemy import select,func
from packages.db.models import Document,Chunk
from packages.db.session import get_db
from services.ingestion.pipeline import ingest_document
from apps.api.schemas.documents import DocumentResponse
router=APIRouter(prefix="/documents",tags=["Documents"])
@router.post("/upload",response_model=DocumentResponse)
async def upload(file:UploadFile=File(...),db=Depends(get_db)):
    data=await file.read()
    if not data:raise HTTPException(400,"Empty file")
    try:d=await ingest_document(db,data,file.filename or "upload",file.content_type or "application/octet-stream")
    except ValueError as e:raise HTTPException(422,str(e))
    n=await db.scalar(select(func.count(Chunk.id)).where(Chunk.document_id==d.id))
    return DocumentResponse(id=str(d.id),filename=d.filename,content_type=d.content_type,size_bytes=d.size_bytes,chunks=int(n or 0))
@router.get("",response_model=list[DocumentResponse])
async def list_docs(db=Depends(get_db)):
    docs=(await db.execute(select(Document).order_by(Document.created_at.desc()))).scalars().all();out=[]
    for d in docs:
        n=await db.scalar(select(func.count(Chunk.id)).where(Chunk.document_id==d.id))
        out.append(DocumentResponse(id=str(d.id),filename=d.filename,content_type=d.content_type,size_bytes=d.size_bytes,chunks=int(n or 0)))
    return out
