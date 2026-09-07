from pydantic import BaseModel,Field
class QueryRequest(BaseModel):query:str=Field(...,min_length=1);top_k:int=Field(5,ge=1,le=20)
class QueryResult(BaseModel):chunk_id:str;document_id:str;filename:str;content:str;retrieval_score:float;rerank_score:float
class QueryResponse(BaseModel):query:str;answer:str|None=None;confidence:float=0.0;citations:list[dict]=[];sources:list[QueryResult];sub_queries:list[str]=[]
