from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.api.chat import router as chat_router
from backend.app.api.history import router as history_router
from backend.app.api.auth import router as auth_router
from backend.app.api.language import router as language_router
from backend.app.api.drafts import router as drafts_router
from backend.app.api.admin import router as admin_router

app = FastAPI(
    title="Melimi Telugu AI",
    description="Backend for a Telugu-oriented chatbot with Melimi conversation mode and knowledge management.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(history_router, prefix="/api/history", tags=["history"])
app.include_router(language_router, prefix="/api/language", tags=["language"])
app.include_router(drafts_router, prefix="/api/drafts", tags=["drafts"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Melimi Telugu AI Backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=int(settings.port), reload=settings.debug)
