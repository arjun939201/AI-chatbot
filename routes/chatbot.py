from fastapi import APIRouter
from pydantic import BaseModel

from chat_history import append_message, load_history, clear_history
from services.grok_chat import chat_with_grok

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(payload: ChatRequest):

    history = load_history()

    append_message("user", payload.message)

    reply = chat_with_grok(
        payload.message,
        history
    )

    append_message("bot", reply)

    return {
        "reply": reply,
        "history": load_history()
    }


@router.post("/clear")
async def clear():
    return {
        "history": clear_history()
    }


@router.get("/history")
async def history():
    return {
        "history": load_history()
    }