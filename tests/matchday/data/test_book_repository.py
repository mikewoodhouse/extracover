import sqlite3

import pytest

from matchday.common.db import initialise_db
from matchday.data import BookRepository
from matchday.models import Book, Team


@pytest.fixture
def repo() -> BookRepository:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    initialise_db(conn)
    return BookRepository(conn)


def test_report_construction(repo: BookRepository):
    assert repo


def test_add(repo: BookRepository):
    book = Book()
    book_count_before = repo.conn.execute("select count(*) from books").fetchone()[0]
    assert repo.add(book)
    book_count_after = repo.conn.execute("select count(*) from books").fetchone()[0]
    assert book_count_after == book_count_before + 1


def test_get(repo: BookRepository):
    book = Book(team_1=Team(name="Banana"))
    book_id = repo.add(book)
    output = repo.get(book_id)
    assert isinstance(output, Book)
    assert output.team_1 == book.team_1


def test_save(repo: BookRepository):
    book = Book(team_1=Team(name="Banana"))
    book_id = repo.add(book)
    book.book_id = book_id
    orange = Team(name="Orange")
    book.team_2 = orange
    repo.save(book)
    from_db = repo.get(book_id)
    assert from_db.team_2 == orange
