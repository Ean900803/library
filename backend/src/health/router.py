from fastapi import APIRouter, Depends
from src.core.database import get_cursor

api_router = APIRouter()

@api_router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck(cursor=Depends(get_cursor)):
    try:
        await cursor.execute("SELECT 1")
        return {
            "status": "ok",
            "db": "connected"
        }
    except Exception:
        return {
            "status": "ok",
            "db": "disconnected"
        }