from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        chunks = []

        if not text.strip():
            return chunks

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks