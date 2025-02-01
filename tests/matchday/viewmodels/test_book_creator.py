import pytest

from matchday.models import Book
from matchday.viewmodels.book_buider import BookBuilder


@pytest.fixture
def creator():
    bc = BookBuilder(Book())
    bc.set_team_name("team_1", "Banana")
    bc.set_team_name("team_2", "Grapefruit")
    return bc


def test_can_construct():
    assert BookBuilder(Book())


def test_setting_team_names(creator):
    assert creator.book.team_1.name == "Banana"
    assert creator.book.team_2.name == "Grapefruit"
