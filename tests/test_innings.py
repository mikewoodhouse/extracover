import pytest

from app.ingest.classes import Innings


@pytest.mark.usefixtures("innings")
def test_to_list_of_database_balls(innings: Innings):
    res = innings.database_balls()
    assert res[0] == {
        "over": 0,
        "ball_seq": 0,
        "ball": 0,
        "bowled_by": "bowler",
        "batter": "batter",
        "non_striker": "non_striker",
        "batter_runs": 1,
        "extra_runs": 1,
        "extra_type": "noball",
        "wicket_fell": False,
        "dismissed": "",
        "how_out": "",
    }
    assert res[1] == {
        "over": 0,
        "ball_seq": 1,
        "ball": 0,
        "bowled_by": "bowler",
        "batter": "batter",
        "non_striker": "non_striker",
        "batter_runs": 0,
        "extra_runs": 0,
        "extra_type": "",
        "wicket_fell": True,
        "dismissed": "batter",
        "how_out": "bowled",
    }
