from fastapi import APIRouter, Cookie, Depends, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.database import get_db
from backend.app.db.models import AnonymousUser

router = APIRouter()


class AnonymousAuthResponse(BaseModel):
    identity_token: str
    message: str


async def get_or_create_anonymous_user(db: AsyncSession, identity_token: str | None):
    from sqlalchemy import select

    if identity_token:
        query = select(AnonymousUser).where(AnonymousUser.identity_token == identity_token)
        result = await db.execute(query)
        user = result.scalars().first()
        if user:
            return user

    new_token = ""
    import secrets
    new_token = secrets.token_urlsafe(32)
    user = AnonymousUser(identity_token=new_token)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/anonymous", response_model=AnonymousAuthResponse)
async def anonymous_identity(response: Response, anon_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)):
    user = await get_or_create_anonymous_user(db, anon_token)
    response.set_cookie("anon_token", user.identity_token, httponly=True, samesite="lax")
    return AnonymousAuthResponse(identity_token=user.identity_token, message="Anonymous identity created or returned.")
