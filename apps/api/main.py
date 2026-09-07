from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from packages.db.init_db import init_db
from apps.api.routes.documents import router as documents_router
from apps.api.routes.query import router as query_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="TraceRAG API",
    version="1.0.0",
    lifespan=lifespan,
)


# Allow the React/Vite frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(documents_router)
app.include_router(query_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "tracerag",
    }