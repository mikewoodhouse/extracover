import pytest

from matchday.models import Book
from matchday.viewmodels.book_creator import BookCreator


@pytest.fixture
def creator():
    bc = BookCreator(Book())
    bc.set_team_name("team_1", "Banana")
    bc.set_team_name("team_2", "Grapefruit")
    return bc


def test_can_construct():
    assert BookCreator(Book())


def test_setting_team_names(creator):
    assert creator.book.team_1.name == "Banana"
    assert creator.book.team_2.name == "Grapefruit"
