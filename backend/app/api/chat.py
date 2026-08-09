from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.db.models import Conversation, Message, AnonymousUser
from backend.app.ai.llm import generate_chat_response

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str
    mode: str | None = None


@router.post("/message")
async def message(payload: ChatRequest, db: AsyncSession = Depends(get_db), anon_token: str | None = Header(default=None)):
    user = await _get_user(db, anon_token)
    if not user:
        return {"error": "Unauthorized"}

    conversation = await _get_or_create_conversation(db, user, payload.conversation_id, payload.mode)

    user_msg = Message(conversation_id=conversation.id, role="user", content=payload.message)
    db.add(user_msg)
    await db.commit()
    await db.refresh(user_msg)

    history = await _load_conversation_messages(db, conversation.id)
    response_text = await generate_chat_response(payload.message, history, conversation.mode)

    bot_msg = Message(conversation_id=conversation.id, role="assistant", content=response_text)
    db.add(bot_msg)
    await db.commit()
    await db.refresh(bot_msg)

    return {
        "conversation_id": str(conversation.id),
        "mode": conversation.mode,
        "message": response_text,
        "messages": [
            {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
            for m in history + [bot_msg]
        ],
    }


async def _get_user(db: AsyncSession, anon_token: str | None) -> AnonymousUser | None:
    if not anon_token:
        return None
    result = await db.execute(select(AnonymousUser).where(AnonymousUser.identity_token == anon_token))
    return result.scalars().first()


async def _get_or_create_conversation(db: AsyncSession, user: AnonymousUser, conversation_id: str | None, mode: str | None) -> Conversation:
    if conversation_id:
        result = await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.owner_id == user.id))
        conversation = result.scalars().first()
        if conversation:
            return conversation

    conversation_mode = mode if mode in ("melimi", "telugu") else "melimi"
    conversation = Conversation(owner_id=user.id, mode=conversation_mode)
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def _load_conversation_messages(db: AsyncSession, conversation_id: str):
    result = await db.execute(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()))
    return result.scalars().all()
