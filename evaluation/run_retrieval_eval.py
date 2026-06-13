import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from agenova.core.schemas import DocumentIn  # noqa: E402
from agenova.memory.embeddings import EmbeddingModel  # noqa: E402
from agenova.memory.graph_store import InMemoryGraphStore  # noqa: E402
from agenova.memory.vector_store import InMemoryVectorStore  # noqa: E402
from agenova.rag.pipeline import RAGPipeline  # noqa: E402


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if k == 0:
        return 0.0
    return sum(1 for doc_id in retrieved[:k] if doc_id in relevant) / k


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    rows = load_jsonl(args.dataset)
    scores: list[float] = []

    for row in rows:
        rag = RAGPipeline(EmbeddingModel("hash"), InMemoryVectorStore(), InMemoryGraphStore())
        rag.ingest([DocumentIn(**document) for document in row["documents"]])
        evidence = rag.retrieve(row["question"], args.top_k)
        retrieved_ids = [item.document_id for item in evidence]
        scores.append(precision_at_k(retrieved_ids, set(row["relevant_doc_ids"]), args.top_k))

    average = sum(scores) / max(len(scores), 1)
    print(json.dumps({"questions": len(rows), f"precision@{args.top_k}": round(average, 4)}, indent=2))


if __name__ == "__main__":
    main()
