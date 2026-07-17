from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    text: str
    vector: list[float]


class LLMResult(BaseModel):
    response: str
    model: str


class DocumentIndexResult(BaseModel):
    document_id: str
    filename: str
    chunks: int
    status: str