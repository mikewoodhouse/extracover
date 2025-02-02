import sqlite3

from matchday.models import Book


class BookRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def add(self, book: Book) -> int:
        csr = self.conn.execute(
            "INSERT INTO books (content) VALUES (:json) RETURNING *",
            {"json": book.to_json()},
        )
        row = csr.fetchone()
        self.conn.commit()
        return row[0]

    def save(self, book: Book) -> None:
        self.conn.execute(
            "UPDATE books SET content = :content WHERE book_id = :book_id",
            {
                "content": book.to_json(),
                "book_id": book.book_id,
            },
        )
        self.conn.commit()

    def get(self, book_id: int) -> Book:
        csr = self.conn.execute(
            "SELECT content FROM books WHERE book_id = :book_id",
            {"book_id": book_id},
        )
        row = csr.fetchone()
        if row:
            return Book.from_json(row["content"])

        return Book()
