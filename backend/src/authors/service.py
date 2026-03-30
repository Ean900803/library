from src.authors import repository
from src.exceptions import NotFoundError

async def create(cursor, name: str):
    new_id = await repository.create(cursor, name)
    return await repository.find_by_id(cursor, new_id)

async def all(cursor):
    return await repository.all(cursor)

async def find_by_id(cursor, id: int):
    result = await repository.find_by_id(cursor, id)
    if result is None:
        raise NotFoundError(f"Author with id {id} not found")
    return result

async def update(cursor, id: int, name: str):
    affected = await repository.update(cursor, id, name)
    if affected == 0:
        raise NotFoundError(f"Author with id {id} not found")
    return await repository.find_by_id(cursor, id)

async def delete(cursor, id: int):
    affected = await repository.delete(cursor, id)
    if affected == 0:
        raise NotFoundError(f"Author with id {id} not found")