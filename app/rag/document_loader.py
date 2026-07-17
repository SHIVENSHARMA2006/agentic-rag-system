from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:
    @staticmethod
    def load_document(file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return DocumentLoader._load_txt(path)

        elif suffix == ".pdf":
            return DocumentLoader._load_pdf(path)

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _load_txt(path: Path) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def _load_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)