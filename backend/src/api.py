# src/api.py
from fastapi import APIRouter
from src.publishers.router import router as publishers_router
from src.authors.router import router as authors_router
# from src.books.router import router as books_router
# from src.members.router import router as members_router
# from src.auth.router import router as auth_router
# from src.rentals.router import router as rentals_router
from src.health.router import api_router as health_router

api_router = APIRouter()
api_router.include_router(health_router)

# 不需要驗證
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# 需要驗證的（之後加 JWT）
api_router.include_router(publishers_router)
api_router.include_router(authors_router)
# api_router.include_router(books_router, prefix="/books", tags=["books"])
# api_router.include_router(members_router, prefix="/members", tags=["members"])
# api_router.include_router(rentals_router, prefix="/rentals", tags=["rentals"])