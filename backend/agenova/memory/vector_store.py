from dataclasses import dataclass, field
from typing import Any
import numpy as np


@dataclass
class VectorRecord:
    document_id: str
    chunk_id: str
    text: str
    vector: np.ndarray
    metadata: dict[str, Any] = field(default_factory=dict)


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    def add(self, records: list[VectorRecord]) -> None:
        self._records.extend(records)

    def search(self, query_vector: np.ndarray, top_k: int) -> list[tuple[VectorRecord, float]]:
        if not self._records:
            return []
        scores: list[tuple[VectorRecord, float]] = []
        for record in self._records:
            score = float(np.dot(record.vector, query_vector))
            scores.append((record, score))
        scores.sort(key=lambda item: item[1], reverse=True)
        return scores[:top_k]

    @property
    def count(self) -> int:
        return len(self._records)

    @property
    def document_count(self) -> int:
        return len({record.document_id for record in self._records})
