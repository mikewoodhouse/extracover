import pytest

from matchday.models import Ball, Player
from matchday.models.ball import Extra, HowOut


@pytest.mark.parametrize(
    "ball,expected_runs_scored,expected_runs_conceded,expected_wickets,expected_is_out",
    [
        (Ball(batter_runs=3, extra_runs=2, extra_type=Extra.NOBALL), 3, 5, 0, False),
        (
            Ball(batter_runs=0, extra_runs=0, extra_type=Extra.NO_EXTRA, how_out=HowOut.BOWLED, striker_out=True),
            0,
            0,
            1,
            True,
        ),
        (
            Ball(batter_runs=0, extra_runs=0, extra_type=Extra.NO_EXTRA, how_out=HowOut.RUN_OUT, striker_out=True),
            0,
            0,
            0,
            True,
        ),
    ],
)
def test_player_updates(ball, expected_runs_scored, expected_runs_conceded, expected_wickets, expected_is_out):
    striker = Player()
    striker.update_as_striker(ball)
    assert striker.runs_scored == expected_runs_scored
    assert striker.is_out == expected_is_out
    bowler = Player()
    bowler.update_as_bowler(ball)
    assert bowler.runs_conceded == expected_runs_conceded
    assert bowler.wickets == expected_wickets
