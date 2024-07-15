import pytest

from app.model import Ball, Player, Scorebook, Team


def fake_team() -> Team:
    return Team(
        [Player() for _ in range(11)],
        [Player() for _ in range(6)],
    )


def fake_book() -> Scorebook:
    return Scorebook(teams=[fake_team(), fake_team()])


def test_creation():
    book = fake_book()
    assert book
    assert isinstance(book.teams, list)
    assert all(isinstance(team, Team) for team in book.teams)
    assert len(book.teams) == 2
    assert all(
        isinstance(player, Player)
        for team in book.teams
        for player in team.batting_order
    )
    assert all(
        isinstance(player, Player)
        for team in book.teams
        for player in team.bowling_order
    )


@pytest.mark.parametrize(
    "ball,expected_total,expected_balls_bowled",
    [
        (Ball(batter_runs=0), 0, 1),
        (Ball(batter_runs=1), 1, 1),
        (Ball(extra_runs=1, wide=True), 1, 0),
    ],
)
def test_adding_balls_to_total(ball, expected_total, expected_balls_bowled):
    book = fake_book()
    book.record_ball(ball)
    assert book.totals[0] == expected_total
    assert book.balls_bowled == expected_balls_bowled
