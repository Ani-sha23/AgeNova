from dataclasses import dataclass
from time import perf_counter

from agenova.agents.llm import LLMProvider
from agenova.core.schemas import AgentRunResponse, AgentTrace
from agenova.rag.pipeline import RAGPipeline


@dataclass
class AgentSpec:
    name: str
    role: str
    goal: str


class DynamicAgentFactory:
    DEFAULT_ROLES = [
        ("NovaPlanner", "planner", "Break the user task into concrete reasoning steps."),
        ("NovaResearcher", "researcher", "Ground the answer in retrieved evidence."),
        ("NovaCritic", "critic", "Challenge weak claims and missing context."),
        ("NovaSynthesizer", "synthesizer", "Merge agent outputs into a concise final response."),
        ("NovaOps", "deployment analyst", "Consider runtime, monitoring, and delivery risks."),
        ("NovaMemory", "memory curator", "Identify durable facts for long-term memory."),
    ]

    def build(self, task: str, max_agents: int) -> list[AgentSpec]:
        lowered = task.lower()
        roles = self.DEFAULT_ROLES[:max_agents]
        if "deploy" in lowered and max_agents >= 3:
            roles[-1] = self.DEFAULT_ROLES[4]
        return [AgentSpec(name=name, role=role, goal=goal) for name, role, goal in roles]


class AgentOrchestrator:
    def __init__(self, rag: RAGPipeline, llm: LLMProvider) -> None:
        self.rag = rag
        self.llm = llm
        self.factory = DynamicAgentFactory()

    def run(self, task: str, max_agents: int, top_k: int) -> AgentRunResponse:
        started = perf_counter()
        evidence = self.rag.retrieve(task, top_k)
        specs = self.factory.build(task, max_agents)
        traces: list[AgentTrace] = []

        for spec in specs:
            answer = self.llm.generate(spec.role, task, evidence)
            confidence = self._confidence(spec.role, answer, evidence)
            traces.append(
                AgentTrace(
                    agent=spec.name,
                    role=spec.role,
                    answer=answer,
                    confidence=confidence,
                    evidence_ids=[item.chunk_id for item in evidence],
                )
            )

        consensus_score = round(sum(trace.confidence for trace in traces) / max(len(traces), 1), 3)
        final_answer = self._synthesize(task, traces, consensus_score)
        latency_ms = (perf_counter() - started) * 1000
        return AgentRunResponse(
            task=task,
            final_answer=final_answer,
            consensus_score=consensus_score,
            agents=traces,
            evidence=evidence,
            latency_ms=latency_ms,
        )

    @staticmethod
    def _confidence(role: str, answer: str, evidence: list) -> float:
        base = 0.62 + min(len(evidence), 5) * 0.05
        if role in {"critic", "researcher"}:
            base += 0.04
        if len(answer) > 240:
            base += 0.03
        return round(min(base, 0.94), 3)

    @staticmethod
    def _synthesize(task: str, traces: list[AgentTrace], consensus_score: float) -> str:
        strongest = sorted(traces, key=lambda trace: trace.confidence, reverse=True)[:2]
        roles = ", ".join(trace.role for trace in strongest)
        return (
            f"AgeNova reached consensus score {consensus_score:.2f} for: {task}. "
            f"The strongest signals came from {roles}. "
            "Final response: use the retrieved evidence as grounding, compare agent perspectives, "
            "and ship the answer with traceable memory references."
        )
