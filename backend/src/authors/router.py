from fastapi import APIRouter
from src.dependencies import CursorDep
from src.authors import service
from src.authors.schema import AuthorCreate, AuthorUpdate, Author, AuthorListResponse

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/")
async def get_authors(cursor: CursorDep):
    return await service.all(cursor)

@router.get("/{id}")
async def get_author(id: int, cursor: CursorDep):
    return await service.find_by_id(cursor, id)

@router.post("/")
async def create_author(author: AuthorCreate, cursor: CursorDep):
    return await service.create(cursor, author.name)

@router.put("/{id}")
async def update_author(id: int, author: AuthorUpdate, cursor: CursorDep):
    return await service.update(cursor, id, author.name)

@router.delete("/{id}", status_code=204)
async def delete_author(id: int, cursor: CursorDep):
    await service.delete(cursor, id)