import sqlite3
from pathlib import Path

import pytest  # noqa: F401

from matchday.data import BookRepository
from matchday.models import Book
from matchday.viewmodels.book_builder import BookBuilder


def memory_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    schema = (Path(__file__).parent.parent.parent.parent / "matchday" / "books_schema.sql").read_text()
    conn.executescript(schema)
    return conn


def memory_repo() -> BookRepository:
    return BookRepository(memory_db())


@pytest.fixture
def builder():
    repo = memory_repo()
    bc = BookBuilder(book=Book(), repo=repo)
    bc.set_team_name("team_1", "Banana")
    bc.set_team_name("team_2", "Grapefruit")
    return bc


def test_can_construct(builder: BookBuilder):
    assert builder


def test_setting_team_names(builder: BookBuilder):
    assert builder.book.team_1.name == "Banana"
    assert builder.book.team_2.name == "Grapefruit"


def test_saving_via_repo(builder: BookBuilder):
    book_id = builder.add()
    assert isinstance(book_id, int)
    assert book_id >= 1


def test_inserting(builder: BookBuilder):
    builder.repo = memory_repo()
    book_id = builder.add()
    assert book_id > 0
    book = builder.repo.get(book_id)
    assert book.team_1.name == builder.book.team_1.name
