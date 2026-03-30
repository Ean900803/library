from fastapi import APIRouter
from src.dependencies import CursorDep
from src.publishers import service
from src.publishers.schema import PublisherCreate, PublisherUpdate, Publisher, PublisherListResponse

router = APIRouter(prefix="/publishers", tags=["publishers"])


@router.get("/", response_model=PublisherListResponse)
async def get_publishers(cursor: CursorDep):
    return PublisherListResponse(data=await service.all(cursor))


@router.get("/{id}", response_model=Publisher)
async def get_publisher(id: int, cursor: CursorDep):
    return await service.find_by_id(cursor, id)


@router.post("/", response_model=Publisher, status_code=201)
async def create_publisher(body: PublisherCreate, cursor: CursorDep):
    return await service.create(cursor, body.name)


@router.put("/{id}", response_model=Publisher)
async def update_publisher(id: int, body: PublisherUpdate, cursor: CursorDep):
    return await service.update(cursor, id, body.name)


@router.delete("/{id}", status_code=204)
async def delete_publisher(id: int, cursor: CursorDep):
    await service.delete(cursor, id)
