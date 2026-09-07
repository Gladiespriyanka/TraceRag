from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    app_name:str="TraceRAG"; app_env:str="development"
    database_url:str="postgresql+asyncpg://tracerag:tracerag@localhost:5432/tracerag"
    redis_url:str="redis://localhost:6379/0"
    embedding_model:str="sentence-transformers/all-MiniLM-L6-v2"; embedding_dimension:int=384; embedding_device:str="cpu"
    reranker_model:str="cross-encoder/ms-marco-MiniLM-L6-v2"; reranker_device:str="cpu"
    gemini_api_key:str=""; gemini_model:str="gemini-2.5-flash"; max_upload_mb:int=25
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")
@lru_cache
def get_settings(): return Settings()
settings=get_settings()
