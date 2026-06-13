from agenova.core.schemas import Evidence


class LLMProvider:
    def generate(self, role: str, task: str, evidence: list[Evidence]) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    def generate(self, role: str, task: str, evidence: list[Evidence]) -> str:
        snippets = " ".join(item.text[:180] for item in evidence[:2])
        if not snippets:
            snippets = "No external evidence was retrieved, so this answer is based on task analysis."
        return (
            f"As the {role}, I address the task: {task}. "
            f"Relevant context: {snippets} "
            "Recommendation: combine retrieved evidence, role-specific reasoning, and consensus checks."
        )
