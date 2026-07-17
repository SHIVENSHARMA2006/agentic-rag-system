from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)

from app.core.logging import logger
from app.core.settings import settings
from app.services.document_indexing_service import (
    DocumentIndexingService,
)

router = APIRouter(tags=["Upload"])

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".csv",
    ".txt",
    ".md",
}

indexing_service = DocumentIndexingService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload a document and immediately index it.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}",
        )

    file_path = UPLOAD_DIR / file.filename

    try:

        logger.info(
            f"Receiving file: {file.filename}"
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = indexing_service.index_document(
            file_path=str(file_path),
            filename=file.filename,
        )

        logger.success(
            f"{file.filename} indexed successfully."
        )

        return {
            "success": True,
            "message": "Document indexed successfully.",
            "data": result,
        }

    except Exception as e:

        logger.exception(e)

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )