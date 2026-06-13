from agenova.agents.llm import MockLLMProvider
from agenova.agents.orchestrator import AgentOrchestrator
from agenova.core.schemas import DocumentIn
from agenova.memory.embeddings import EmbeddingModel
from agenova.memory.graph_store import InMemoryGraphStore
from agenova.memory.vector_store import InMemoryVectorStore
from agenova.rag.pipeline import RAGPipeline


def test_agent_orchestrator_returns_consensus():
    rag = RAGPipeline(EmbeddingModel("hash"), InMemoryVectorStore(), InMemoryGraphStore())
    rag.ingest([DocumentIn(id="one", text="AgeNova coordinates planner and critic agents.")])
    response = AgentOrchestrator(rag, MockLLMProvider()).run(
        "Explain AgeNova agent coordination.", max_agents=3, top_k=2
    )
    assert response.consensus_score > 0
    assert len(response.agents) == 3
    assert "AgeNova reached consensus" in response.final_answer
