from typing import Any
from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    documents: list[DocumentIn]


class IngestResponse(BaseModel):
    accepted: int
    chunks_indexed: int
    graph_edges: int


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class Evidence(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    query: str
    evidence: list[Evidence]


class AgentRunRequest(BaseModel):
    task: str
    max_agents: int = Field(default=3, ge=1, le=6)
    top_k: int = Field(default=5, ge=1, le=10)


class AgentTrace(BaseModel):
    agent: str
    role: str
    answer: str
    confidence: float
    evidence_ids: list[str]


class AgentRunResponse(BaseModel):
    task: str
    final_answer: str
    consensus_score: float
    agents: list[AgentTrace]
    evidence: list[Evidence]
    latency_ms: float


class MemoryStats(BaseModel):
    documents: int
    chunks: int
    graph_nodes: int
    graph_edges: int
