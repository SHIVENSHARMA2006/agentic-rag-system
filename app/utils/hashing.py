import hashlib
from pathlib import Path


def generate_sha256(file_path: str) -> str:
    """
    Generate SHA256 hash of a file.
    """

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            data = f.read(8192)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


def document_id(file_path: str) -> str:
    """
    Generate deterministic document id.
    """

    return generate_sha256(file_path)