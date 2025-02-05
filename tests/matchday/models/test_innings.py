import pytest

from matchday.models.ball import Ball
from matchday.models.innings import Innings


def test_can_construct():
    assert Innings()


def test_dot_ball():
    inns = Innings()
    ball = Ball(batter_runs=1)
    inns.update(ball)
    assert inns.total == 1


@pytest.mark.parametrize(
    "ball,total",
    [
        (Ball(batter_runs=1), 1),
        (Ball(extra_runs=1), 1),
        (Ball(penalty_runs=1), 1),
    ],
)
def test_ball_updates_score(ball: Ball, total: int):
    inns = Innings()
    inns.update(ball)
    assert inns.total == total


@pytest.mark.parametrize(
    "ball,wickets",
    [
        (Ball(striker_out=True), 1),
        (Ball(), 0),
        (Ball(non_striker_out=True), 1),
    ],
)
def test_ball_updates_wickets(ball: Ball, wickets: int):
    inns = Innings()
    inns.update(ball)
    assert inns.wickets == wickets
