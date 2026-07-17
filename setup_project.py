from pathlib import Path

# Project root folder (change this if your folder name is different)
project_root = Path("agentic-rag-system")

# Folder structure
folders = [
    "app",
    "app/api",
    "app/agents",
    "app/core",
    "app/rag",
    "app/memory",
    "app/services",
    "app/models",
    "tests",
]

# Files to create
files = {
    ".env": "",
    ".gitignore": """venv/
__pycache__/
*.pyc
.env
.idea/
.vscode/
""",
    "requirements.txt": """fastapi
uvicorn
langchain
langgraph
qdrant-client
openai
google-generativeai
redis
psycopg2-binary
tavily-python
trafilatura
python-dotenv
""",
    "README.md": "# Agentic RAG System\n",
    "main.py": """from fastapi import FastAPI

app = FastAPI(title="Agentic RAG System")

@app.get("/")
def root():
    return {"message": "Agentic RAG API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
""",

    "app/__init__.py": "",
    "app/api/__init__.py": "",
    "app/agents/__init__.py": "",
    "app/core/__init__.py": "",
    "app/rag/__init__.py": "",
    "app/memory/__init__.py": "",
    "app/services/__init__.py": "",
    "app/models/__init__.py": "",

    "app/api/routes.py": "",
    "app/agents/query_agent.py": "",
    "app/agents/router_agent.py": "",
    "app/agents/retriever_agent.py": "",
    "app/agents/web_agent.py": "",
    "app/agents/verifier_agent.py": "",
    "app/agents/response_agent.py": "",

    "app/core/config.py": "",
    "app/core/constants.py": "",
    "app/core/utils.py": "",

    "app/rag/chunker.py": "",
    "app/rag/embedder.py": "",
    "app/rag/vector_store.py": "",

    "app/memory/session_memory.py": "",
    "app/memory/chat_history.py": "",

    "app/services/gemini_service.py": "",
    "app/services/tavily_service.py": "",
    "app/services/qdrant_service.py": "",

    "app/models/request_models.py": "",
    "app/models/response_models.py": "",

    "tests/test_api.py": "",
}

# Create root
project_root.mkdir(exist_ok=True)

# Create folders
for folder in folders:
    (project_root / folder).mkdir(parents=True, exist_ok=True)

# Create files
for filepath, content in files.items():
    file_path = project_root / filepath
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

print("Project structure created successfully!")