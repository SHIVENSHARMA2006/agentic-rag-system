from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Agentic RAG System"
    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    GOOGLE_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    TAVILY_API_KEY: str = ""

    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "agentic_rag_docs"

    DATABASE_URL: str = ""
    REDIS_URL: str = ""

    MAX_UPLOAD_SIZE_MB: int = 50
    UPLOAD_DIR: str = "uploads"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    TOP_K_RETRIEVAL: int = 5
    MAX_RETRIEVAL_CHUNKS: int = 5

    MAX_WEB_RESULTS: int = 3

    MAX_CONTEXT_LENGTH: int = 8000

    MAX_CHUNK_LENGTH: int = 1200

    MAX_WEB_CONTENT_LENGTH: int = 1000

    


    LLM_MODEL: str = "openai/gpt-oss-120b"
    EMBEDDING_MODEL: str = "text-embedding-004"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    MAX_RETRIEVAL_CHUNKS: int = 5

    MAX_WEB_RESULTS: int = 3

    MAX_CONTEXT_LENGTH: int = 8000

    MAX_CHUNK_LENGTH: int = 1200

    MAX_WEB_CONTENT_LENGTH: int = 1000


settings = Settings()
