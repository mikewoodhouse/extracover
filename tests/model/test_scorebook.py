import pytest

from app.model import Ball, InningsCard, Player, Scorebook


def fake_player() -> Player:
    return Player()


def fake_innings() -> InningsCard:
    return InningsCard(batters=[fake_player()] * 11)


@pytest.fixture
def book() -> Scorebook:
    return Scorebook(first_innings=fake_innings())


def test_creation(book: Scorebook):
    assert book
    assert book.current_innings.striker_index == 0
    assert book.current_innings.non_striker_index == 1


@pytest.mark.parametrize(
    "ball,expected_total,expected_balls_bowled,wickets_down",
    [
        (Ball(batter_runs=0), 0, 1, 0),
        (Ball(batter_runs=1), 1, 1, 0),
        (Ball(extra_runs=1, wide=True), 1, 0, 0),
        (Ball(extra_runs=1, noball=True), 1, 0, 0),
        (Ball(extra_runs=1, bye=True), 1, 1, 0),
        (Ball(wicket_fell=True), 0, 1, 1),
    ],
)
def test_first_ball_first_innings(
    book: Scorebook, ball, expected_total, expected_balls_bowled, wickets_down
):
    book.update(ball)
    assert book.current_innings.total == expected_total
    assert book.current_innings.balls_bowled == expected_balls_bowled
    assert book.current_innings.wickets == wickets_down


@pytest.mark.parametrize(
    "ball,bowled,wickets",
    [
        (Ball(), 119, 0),
        (Ball(wicket_fell=True), 1, 9),
    ],
)
def test_closing_first_innings(book: Scorebook, ball: Ball, bowled: int, wickets: int):
    book.current_innings.balls_bowled = bowled
    book.current_innings.wickets = wickets
    book.update(ball)
    assert book.first_innings.closed
    assert book.current_innings == book.second_innings


@pytest.mark.parametrize(
    "ball,striker,non_striker,striker_runs",
    [
        (Ball(), 0, 1, 0),
    ],
)
def test_batters_update_correctly(
    book: Scorebook, ball, striker, non_striker, striker_runs
):
    book.update(ball)
    inns = book.current_innings
    assert inns.striker_index == striker
    assert inns.non_striker_index == non_striker
    assert inns.striker.runs_scored == striker_runs
