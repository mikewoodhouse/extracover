import pytest

from app.model import Ball, Scorebook


@pytest.fixture
def fake_book() -> Scorebook:
    return Scorebook()


def test_creation(fake_book):
    assert fake_book


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
def test_adding_balls_to_total(
    ball, expected_total, expected_balls_bowled, wickets_down
):
    pass
