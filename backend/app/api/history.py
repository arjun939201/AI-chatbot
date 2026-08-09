from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app.db.database import get_db
from backend.app.db.models import Conversation, Message, AnonymousUser

router = APIRouter()


async def get_current_user(db: AsyncSession, anon_token: str | None = Header(default=None)) -> AnonymousUser | None:
    if not anon_token:
        return None
    result = await db.execute(select(AnonymousUser).where(AnonymousUser.identity_token == anon_token))
    return result.scalars().first()


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db), anon_token: str | None = Header(default=None)):
    user = await get_current_user(db, anon_token)
    if not user:
        return {"conversations": []}

    result = await db.execute(select(Conversation).where(Conversation.owner_id == user.id).order_by(Conversation.updated_at.desc()))
    conversations = result.scalars().all()
    return {
        "conversations": [
            {
                "id": str(item.id),
                "title": item.title,
                "mode": item.mode,
                "updated_at": item.updated_at.isoformat(),
            }
            for item in conversations
        ]
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db), anon_token: str | None = Header(default=None)):
    user = await get_current_user(db, anon_token)
    if not user:
        return {"error": "Unauthorized"}

    result = await db.execute(select(Conversation).where(Conversation.id == conversation_id, Conversation.owner_id == user.id))
    conversation = result.scalars().first()
    if not conversation:
        return {"error": "Conversation not found"}

    messages_result = await db.execute(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc()))
    messages = messages_result.scalars().all()
    return {
        "conversation": {
            "id": str(conversation.id),
            "title": conversation.title,
            "mode": conversation.mode,
            "messages": [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in messages],
        }
    }
