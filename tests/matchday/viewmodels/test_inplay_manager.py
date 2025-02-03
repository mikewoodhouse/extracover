from matchday.models import Book, Team
from matchday.viewmodels import InplayManager


def fake_team(name: str) -> Team:
    return Team(name=name)


def test_can_create():
    assert InplayManager(Book())


def test_title():
    team_1 = fake_team("Abc")
    team_2 = fake_team("Def")
    book = Book(team_1=team_1, team_2=team_2)
    mgr = InplayManager(book)
    assert mgr.title == f"{team_1.name} vs {team_2.name}"
