import pytest

from app.ingest.classes import Delivery, Dismissal, Extras, Innings, Over, Runs


@pytest.fixture
def innings() -> Innings:
    return Innings(
        overs=[
            Over(
                over=0,
                deliveries=[
                    Delivery(
                        batter="batter",
                        bowler="bowler",
                        non_striker="non_striker",
                        runs=Runs(batter=1, extras=1, total=2),
                        extras=Extras(noballs=1),
                    ),
                    Delivery(
                        batter="batter",
                        bowler="bowler",
                        non_striker="non_striker",
                        wickets=[
                            Dismissal(
                                player_out="batter",
                                kind="bowled",
                            ),
                        ],
                    ),
                ],
            )
        ]
    )
