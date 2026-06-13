from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

from agenova.agents.llm import MockLLMProvider
from agenova.agents.orchestrator import AgentOrchestrator
from agenova.core.config import get_settings
from agenova.core.schemas import (
    AgentRunRequest,
    AgentRunResponse,
    IngestRequest,
    IngestResponse,
    MemoryStats,
    QueryRequest,
    QueryResponse,
)
from agenova.memory.embeddings import EmbeddingModel
from agenova.memory.graph_store import InMemoryGraphStore
from agenova.memory.vector_store import InMemoryVectorStore
from agenova.rag.pipeline import RAGPipeline

settings = get_settings()
embeddings = EmbeddingModel(settings.embedding_model, settings.use_sentence_transformers)
vector_store = InMemoryVectorStore()
graph_store = InMemoryGraphStore()
rag = RAGPipeline(
    embeddings=embeddings,
    vector_store=vector_store,
    graph_store=graph_store,
    max_chunk_chars=settings.max_chunk_chars,
    chunk_overlap=settings.chunk_overlap,
)
orchestrator = AgentOrchestrator(rag=rag, llm=MockLLMProvider())

REQUESTS = Counter("agenova_requests_total", "Total API requests", ["endpoint"])
LATENCY = Histogram("agenova_agent_latency_ms", "Agent workflow latency in milliseconds")

app = FastAPI(title="AgeNova API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    REQUESTS.labels(endpoint="health").inc()
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}


@app.post("/v1/documents/ingest", response_model=IngestResponse)
def ingest_documents(payload: IngestRequest) -> IngestResponse:
    REQUESTS.labels(endpoint="ingest").inc()
    chunks, graph_edges = rag.ingest(payload.documents)
    return IngestResponse(accepted=len(payload.documents), chunks_indexed=chunks, graph_edges=graph_edges)


@app.post("/v1/retrieve", response_model=QueryResponse)
def retrieve(payload: QueryRequest) -> QueryResponse:
    REQUESTS.labels(endpoint="retrieve").inc()
    return QueryResponse(query=payload.query, evidence=rag.retrieve(payload.query, payload.top_k))


@app.post("/v1/agents/run", response_model=AgentRunResponse)
def run_agents(payload: AgentRunRequest) -> AgentRunResponse:
    REQUESTS.labels(endpoint="agents").inc()
    response = orchestrator.run(payload.task, payload.max_agents, payload.top_k)
    LATENCY.observe(response.latency_ms)
    return response


@app.get("/v1/memory/stats", response_model=MemoryStats)
def memory_stats() -> MemoryStats:
    REQUESTS.labels(endpoint="memory_stats").inc()
    return MemoryStats(
        documents=vector_store.document_count,
        chunks=vector_store.count,
        graph_nodes=len(graph_store.nodes),
        graph_edges=len(graph_store.edges),
    )


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain")
