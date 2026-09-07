import uuid
from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from pgvector.sqlalchemy import Vector
from packages.core.config import settings
class Base(DeclarativeBase): pass
class Document(Base):
    __tablename__="documents"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    filename:Mapped[str]=mapped_column(String(500)); content_type:Mapped[str]=mapped_column(String(100)); size_bytes:Mapped[int]=mapped_column(Integer,default=0)
    metadata_json:Mapped[dict]=mapped_column("metadata",JSON,default=dict); access_level:Mapped[str]=mapped_column(String(50),default="public"); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    chunks:Mapped[list["Chunk"]]=relationship(back_populates="document",cascade="all, delete-orphan")
class Chunk(Base):
    __tablename__="chunks"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    document_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("documents.id",ondelete="CASCADE"))
    parent_chunk_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),nullable=True)
    chunk_index:Mapped[int]=mapped_column(Integer); content:Mapped[str]=mapped_column(Text)
    embedding:Mapped[list[float]|None]=mapped_column(Vector(settings.embedding_dimension),nullable=True)
    metadata_json:Mapped[dict]=mapped_column("metadata",JSON,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    document:Mapped["Document"]=relationship(back_populates="chunks")
class EvidenceClaim(Base):
    __tablename__="evidence_claims"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    chunk_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey("chunks.id",ondelete="CASCADE"))
    claim_text:Mapped[str]=mapped_column(Text); claim_type:Mapped[str]=mapped_column(String(30),default="fact")
class GraphEdge(Base):
    __tablename__="graph_edges"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    source_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True)); target_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True))
    edge_type:Mapped[str]=mapped_column(String(30)); weight:Mapped[float]=mapped_column(default=1.0)
