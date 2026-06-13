def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(clean):
        end = min(start + max_chars, len(clean))
        chunk = clean[start:end]
        if end < len(clean):
            split_at = chunk.rfind(" ")
            if split_at > max_chars * 0.65:
                end = start + split_at
                chunk = clean[start:end]
        chunks.append(chunk.strip())
        if end == len(clean):
            break
        start = max(0, end - overlap)
    return chunks
