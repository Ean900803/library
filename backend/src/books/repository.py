from src.books.schema import BookCreate, BookUpdate



async def create(cursor, book: BookCreate):
    await cursor.execute(
        "INSERT INTO books (title, publisher_id, prefix) VALUES (%s, %s, %s)",
        (book.title, book.publisher_id, book.prefix),
    )
    book_id = cursor.lastrowid

    await cursor.executemany(
        "INSERT INTO author_book (book_id, author_id) VALUES (%s, %s)",
        [(book_id, author_id) for author_id in book.author_ids],
    )

    await cursor.executemany(
        "INSERT INTO book_copies (book_id, copy_code) VALUES (%s, %s)",
        [(book_id, f"{book.prefix}-{i + 1:03d}") for i in range(book.copies)],
    )
    return book_id


async def add_copies(cursor, book_id: int, prefix: str, count: int):
    await cursor.execute(
        """
        SELECT COALESCE(
            MAX(CAST(SUBSTRING_INDEX(copy_code, '-', -1) AS UNSIGNED)), 0
        ) AS max_num
        FROM book_copies WHERE book_id = %s
        """,
        (book_id,),
    )
    row = await cursor.fetchone()
    max_num = row["max_num"]

    await cursor.executemany(
        "INSERT INTO book_copies (book_id, copy_code) VALUES (%s, %s)",
        [(book_id, f"{prefix}-{max_num + i + 1:03d}") for i in range(count)],
    )

async def find_by_id(cursor, id: int):
    await cursor.execute("SELECT id, title, prefix FROM books WHERE id = %s", (id,))
    return await cursor.fetchone()

async def book_list(cursor):
    await cursor.execute("SELECT id, title, prefix FROM books")
    return await cursor.fetchall()


async def book_detail(cursor, id: int):
    await cursor.execute(
        """
        SELECT
            b.id,
            b.title,
            b.prefix,
            p.name AS publisher_name,
            GROUP_CONCAT(a.name ORDER BY a.id SEPARATOR ', ') AS authors,
            COUNT(bc.id) AS total_copies,
            SUM(bc.status = 'available') AS available_copies
        FROM books b
        LEFT JOIN publishers p ON b.publisher_id = p.id
        LEFT JOIN author_book ab ON b.id = ab.book_id
        LEFT JOIN authors a ON ab.author_id = a.id
        LEFT JOIN book_copies bc ON b.id = bc.book_id
        WHERE b.id = %s
        GROUP BY b.id, b.title, b.prefix, p.name
        """,
        (id,),
    )
    return await cursor.fetchone()


async def update(cursor, id: int, book: BookUpdate):
    await cursor.execute(
        "UPDATE books SET title = %s, publisher_id = %s, prefix = %s WHERE id = %s",
        (book.title, book.publisher_id, book.prefix, id),
    )
    if cursor.rowcount == 0:
        return 0

    await cursor.execute("DELETE FROM author_book WHERE book_id = %s", (id,))
    await cursor.executemany(
        "INSERT INTO author_book (book_id, author_id) VALUES (%s, %s)",
        [(id, author_id) for author_id in book.author_ids],
    )
    return 1


async def delete(cursor, id: int):
    await cursor.execute("DELETE FROM books WHERE id = %s", (id,))
    return cursor.rowcount
