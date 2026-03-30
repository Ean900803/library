async def all(cursor):
    await cursor.execute("SELECT * FROM publishers")
    return await cursor.fetchall()


async def find_by_id(cursor, id: int):
    await cursor.execute("SELECT * FROM publishers WHERE id = %s", (id,))
    return await cursor.fetchone()


async def create(cursor, name: str):
    await cursor.execute("INSERT INTO publishers (name) VALUES (%s)", (name,))
    return cursor.lastrowid


async def update(cursor, id: int, name: str):
    await cursor.execute(
        "UPDATE publishers SET name = %s WHERE id = %s",
        (name, id),
    )
    return cursor.rowcount


async def delete(cursor, id: int):
    await cursor.execute("DELETE FROM publishers WHERE id = %s", (id,))
    return cursor.rowcount
