from matchday.models import Book
from matchday.viewmodels import InplayManager


def test_can_create():
    assert InplayManager(Book())
