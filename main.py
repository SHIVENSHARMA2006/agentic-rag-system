from fastapi import FastAPI

from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router

app = FastAPI(
    title="Agentic AI RAG Backend",
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(health_router)


@app.get("/")
def root():

    return {
        "message": "Agentic AI RAG API Running"
    }