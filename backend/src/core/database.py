import aiomysql
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import settings

pool: aiomysql.Pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時
    global pool
    pool = await aiomysql.create_pool(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=settings.MYSQL_DATABASE,
        autocommit=False,
        maxsize=10,
    )
    yield
    # 關閉時
    pool.close()
    await pool.wait_closed()

async def get_cursor():
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            try:
                yield cur
                await conn.commit()    # 正常 → commit
            except Exception:
                await conn.rollback()  # 錯誤 → rollback
                raise