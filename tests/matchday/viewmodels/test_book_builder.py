from unittest.mock import Mock

import pytest

from matchday.models import Book
from matchday.viewmodels.book_builder import BookBuilder


@pytest.fixture
def buidler():
    repo = Mock()
    bc = BookBuilder(book=Book(), repo=repo)
    bc.set_team_name("team_1", "Banana")
    bc.set_team_name("team_2", "Grapefruit")
    return bc


def test_can_construct(buidler):
    assert buidler


def test_setting_team_names(buidler):
    assert buidler.book.team_1.name == "Banana"
    assert buidler.book.team_2.name == "Grapefruit"
