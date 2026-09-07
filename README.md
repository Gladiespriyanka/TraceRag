# TraceRAG — Evidence-First Enterprise Research & Decision Intelligence

Full-stack implementation following the supplied seven-phase blueprint.

Backend: FastAPI, PostgreSQL + pgvector, Redis, SQLAlchemy async, SentenceTransformers, Gemini.
Frontend: React + TypeScript + Vite + React Flow.
Core flow: ingestion -> chunking -> embeddings -> lexical/vector retrieval -> RRF -> reranking -> query decomposition -> grounded generation -> citations/confidence.
Also includes evidence claims/graph primitives, NLI wrapper, benchmark scaffolding, Docker and CI.

## Run backend
Copy `.env.example` to `.env`, add GEMINI_API_KEY if desired.
docker compose up -d
python -m pip install -e .
python -m uvicorn apps.api.main:app --reload

API: http://127.0.0.1:8000/docs

## Run frontend
cd apps/web
npm install
npm run dev

UI: http://localhost:5173

No benchmark numbers are fabricated. Run evaluation on your own corpus before publishing metrics.
