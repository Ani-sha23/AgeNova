import hashlib
import numpy as np


class EmbeddingModel:
    def __init__(self, model_name: str, use_sentence_transformers: bool = False):
        self.model_name = model_name
        self.use_sentence_transformers = use_sentence_transformers
        self._model = None
        if use_sentence_transformers:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        if self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=True)
            return np.asarray(vectors, dtype=np.float32)
        return np.vstack([self._hash_embedding(text) for text in texts]).astype(np.float32)

    @staticmethod
    def _hash_embedding(text: str, dimensions: int = 384) -> np.ndarray:
        vector = np.zeros(dimensions, dtype=np.float32)
        tokens = [token.strip(".,:;!?()[]{}").lower() for token in text.split()]
        for token in tokens:
            if not token:
                continue
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
