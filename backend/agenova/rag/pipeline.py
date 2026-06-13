from agenova.core.schemas import DocumentIn, Evidence
from agenova.memory.embeddings import EmbeddingModel
from agenova.memory.graph_store import InMemoryGraphStore
from agenova.memory.vector_store import InMemoryVectorStore, VectorRecord
from agenova.rag.chunking import chunk_text


class RAGPipeline:
    def __init__(
        self,
        embeddings: EmbeddingModel,
        vector_store: InMemoryVectorStore,
        graph_store: InMemoryGraphStore,
        max_chunk_chars: int = 900,
        chunk_overlap: int = 120,
    ) -> None:
        self.embeddings = embeddings
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.max_chunk_chars = max_chunk_chars
        self.chunk_overlap = chunk_overlap

    def ingest(self, documents: list[DocumentIn]) -> tuple[int, int]:
        records: list[VectorRecord] = []
        graph_edges = 0
        for document in documents:
            chunks = chunk_text(document.text, self.max_chunk_chars, self.chunk_overlap)
            vectors = self.embeddings.encode(chunks)
            graph_edges += self.graph_store.ingest_text(document.text, document.id)
            for index, chunk in enumerate(chunks):
                records.append(
                    VectorRecord(
                        document_id=document.id,
                        chunk_id=f"{document.id}:{index}",
                        text=chunk,
                        vector=vectors[index],
                        metadata=document.metadata,
                    )
                )
        self.vector_store.add(records)
        return len(records), graph_edges

    def retrieve(self, query: str, top_k: int) -> list[Evidence]:
        query_vector = self.embeddings.encode([query])[0]
        results = self.vector_store.search(query_vector, top_k)
        return [
            Evidence(
                document_id=record.document_id,
                chunk_id=record.chunk_id,
                text=record.text,
                score=score,
                metadata=record.metadata,
            )
            for record, score in results
        ]
