import re
from collections import Counter, defaultdict


ENTITY_PATTERN = re.compile(r"\b[A-Z][A-Za-z0-9-]{2,}\b")


class InMemoryGraphStore:
    def __init__(self) -> None:
        self.nodes: Counter[str] = Counter()
        self.edges: Counter[tuple[str, str]] = Counter()
        self.sources: dict[tuple[str, str], set[str]] = defaultdict(set)

    def ingest_text(self, text: str, source_id: str) -> int:
        entities = list(dict.fromkeys(ENTITY_PATTERN.findall(text)))
        for entity in entities:
            self.nodes[entity] += 1
        created = 0
        for left_index, left in enumerate(entities):
            for right in entities[left_index + 1 :]:
                edge = tuple(sorted((left, right)))
                if self.edges[edge] == 0:
                    created += 1
                self.edges[edge] += 1
                self.sources[edge].add(source_id)
        return created

    def related(self, entity: str, limit: int = 10) -> list[tuple[str, int]]:
        related: Counter[str] = Counter()
        for (left, right), weight in self.edges.items():
            if left == entity:
                related[right] += weight
            elif right == entity:
                related[left] += weight
        return related.most_common(limit)
