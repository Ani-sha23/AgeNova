import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from agenova.agents.llm import MockLLMProvider  # noqa: E402
from agenova.agents.orchestrator import AgentOrchestrator  # noqa: E402
from agenova.core.schemas import DocumentIn  # noqa: E402
from agenova.memory.embeddings import EmbeddingModel  # noqa: E402
from agenova.memory.graph_store import InMemoryGraphStore  # noqa: E402
from agenova.memory.vector_store import InMemoryVectorStore  # noqa: E402
from agenova.rag.pipeline import RAGPipeline  # noqa: E402


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    args = parser.parse_args()
    rows = load_jsonl(args.dataset)

    rag = RAGPipeline(EmbeddingModel("hash"), InMemoryVectorStore(), InMemoryGraphStore())
    rag.ingest(
        [
            DocumentIn(
                id="agenova-overview",
                text=(
                    "AgeNova uses vector retrieval, graph memory, planner agents, critic agents, "
                    "consensus debate, Docker deployment, a FastAPI API, and a Next.js dashboard."
                ),
            )
        ]
    )
    orchestrator = AgentOrchestrator(rag, MockLLMProvider())

    completed = 0
    consensus_scores: list[float] = []
    for row in rows:
        response = orchestrator.run(row["task"], max_agents=3, top_k=5)
        text = response.final_answer.lower() + " " + " ".join(agent.answer.lower() for agent in response.agents)
        matched = sum(1 for keyword in row["expected_keywords"] if keyword.lower() in text)
        completed += int(matched >= 2)
        consensus_scores.append(response.consensus_score)

    print(
        json.dumps(
            {
                "tasks": len(rows),
                "completion_rate": round(completed / max(len(rows), 1), 4),
                "mean_consensus": round(sum(consensus_scores) / max(len(consensus_scores), 1), 4),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
