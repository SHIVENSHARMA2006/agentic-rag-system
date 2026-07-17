import uuid
from pathlib import Path

from qdrant_client.models import PointStruct

from app.core.logging import logger

from app.repositories.vector_repository import VectorRepository

from app.services.embedding_service import EmbeddingService
from app.services.parser_service import ParserService

from app.utils.chunking import split_text
from app.utils.hashing import (
    document_id,
    generate_sha256,
)
from app.utils.metadata import build_metadata


class DocumentIndexingService:
    """
    Complete document ingestion pipeline.

    Upload

        ↓

    Parse

        ↓

    Chunk

        ↓

    Embed

        ↓

    Store
    """

    def __init__(self):

        self.parser = ParserService()

        self.embedder = EmbeddingService()

        self.repository = VectorRepository()

    def index_document(
        self,
        file_path: str,
        filename: str,
    ):

        logger.info(f"Indexing document: {filename}")
        logger.info("Step 1: Parsing")
        text = self.parser.parse(file_path)

        if not text.strip():

            raise ValueError(
                "Document contains no readable text."
            )
        logger.info("Step 2: Chunking")
        chunks = split_text(text)

        if not chunks:

            raise ValueError(
                "No chunks generated."
            )
        logger.info("Step 3: Embeddings")
        total_chunks = len(chunks)

        logger.info(
            f"Generated {total_chunks} chunks."
        )

        doc_hash = generate_sha256(file_path)

        doc_id = document_id(file_path)

        points = []

        for index, chunk in enumerate(chunks):

            embedding = self.embedder.embed(chunk)

            metadata = build_metadata(
                document_id=doc_id,
                filename=filename,
                chunk_index=index,
                total_chunks=total_chunks,
                document_hash=doc_hash,
            )

            payload = {
                "text": chunk,
                **metadata,
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )

        logger.info(
            f"Uploading {len(points)} vectors to Qdrant..."
        )
        logger.info("Step 4: Uploading to Qdrant")
        self.repository.insert_batch(points)

        logger.success(
            f"Indexed '{filename}' successfully."
        )

        return {
            "status": "success",
            "document_id": doc_id,
            "filename": filename,
            "chunks": total_chunks,
            "characters": len(text),
            "hash": doc_hash,
        }

    def index_path(
        self,
        file_path: str,
    ):
        """
        Convenience wrapper.
        """

        return self.index_document(
            file_path=file_path,
            filename=Path(file_path).name,
        )