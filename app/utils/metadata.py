from datetime import datetime

from app.core.constants import METADATA_VERSION


def build_metadata(
    document_id: str,
    filename: str,
    chunk_index: int,
    total_chunks: int,
    document_hash: str,
):

    return {
        "document_id": document_id,
        "filename": filename,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
        "hash": document_hash,
        "metadata_version": METADATA_VERSION,
        "created_at": datetime.utcnow().isoformat(),
    }