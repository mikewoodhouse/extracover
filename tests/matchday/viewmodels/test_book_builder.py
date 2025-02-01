import sqlite3

import pytest  # noqa: F401

from matchday.data import BookRepository
from matchday.models import Book
from matchday.viewmodels.book_builder import BookBuilder


@pytest.fixture
def builder(mocker):
    repo = BookRepository(sqlite3.connect(":memory:"))
    mocker.patch("matchday.data.BookRepository.add").return_value = 1
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
