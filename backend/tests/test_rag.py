from agenova.core.config import Settings
from agenova.core.schemas import DocumentIn
from agenova.memory.embeddings import EmbeddingModel
from agenova.memory.graph_store import InMemoryGraphStore
from agenova.memory.vector_store import InMemoryVectorStore
from agenova.rag.pipeline import RAGPipeline


def test_rag_ingest_and_retrieve():
    settings = Settings()
    rag = RAGPipeline(
        embeddings=EmbeddingModel(settings.embedding_model),
        vector_store=InMemoryVectorStore(),
        graph_store=InMemoryGraphStore(),
    )
    chunks, edges = rag.ingest(
        [
            DocumentIn(
                id="demo",
                text="AgeNova uses Vector Memory and Graph Memory for retrieval augmented generation.",
            )
        ]
    )
    evidence = rag.retrieve("What memory does AgeNova use?", top_k=3)
    assert chunks >= 1
    assert edges >= 1
    assert evidence
    assert evidence[0].document_id == "demo"
