from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def admin_status():
    return {"admin": "available", "notes": "Admin workflows are not implemented yet."}
