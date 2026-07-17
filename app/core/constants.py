"""
Application-wide constants.
"""

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".csv",
    ".txt",
    ".md",
}

CHUNK_SIZE = 800

CHUNK_OVERLAP = 150

METADATA_VERSION = 1

HASH_ALGORITHM = "sha256"

MAX_FILENAME_LENGTH = 255