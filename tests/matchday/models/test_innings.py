import pytest

from matchday.models.ball import Ball
from matchday.models.innings import Innings
from matchday.models.player import Player
from matchday.models.team import Team


def fake_innings():
    return Innings(
        batting=Team(
            players={
                -1: Player(),
            }
        ),
        bowling=Team(
            players={
                -1: Player(),
            }
        ),
    )


def test_can_construct():
    assert Innings()


def test_dot_ball():
    inns = fake_innings()
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
    inns = fake_innings()
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
    inns = fake_innings()
    inns.update(ball)
    assert inns.wickets == wickets
