import random
import string

import pytest

from app.ingest.classes import (Delivery, Dismissal, Extras, Info, Innings,
                                Match, Meta, Over, Registry, Runs)


def fake_meta() -> Meta:
    return Meta()


def fake_name() -> str:
    chars = string.ascii_lowercase

    def part(k: int) -> str:
        return "".join(random.choices(chars, k=k))

    return f"{part(4)} {part(6)}"


def fake_reg() -> str:
    chars = list("0123456789abcdef")
    return "".join(random.choices(chars, k=8))


def fake_info() -> Info:
    teams = ["TeamA", "TeamB"]
    players = {team: [fake_name() for _ in range(11)] for team in teams}
    registry = Registry(
        people={
            player: fake_reg()
            for team_sheet in players.values()
            for player in team_sheet
        }
    )
    # add 2 fake umpires - not in teams
    registry.people[fake_name()] = fake_reg()
    registry.people[fake_name()] = fake_reg()
    return Info(
        registry=registry,
        players=players,
        teams=teams,
    )


def fake_over(num: int) -> Over:
    return Over(
        over=num,
        deliveries=[
            Delivery(ball_seq=0, legal_ball_seq=0, runs=Runs(batter=0, total=0)),
            Delivery(ball_seq=1, legal_ball_seq=1, runs=Runs(batter=1, total=1)),
        ],
    )


def fake_innings(team: str, num_overs: int = 2) -> Innings:
    return Innings(
        team=team, overs=[fake_over(over_num) for over_num in range(num_overs)]
    )


@pytest.fixture
def fake_match() -> Match:
    meta = fake_meta()
    info = fake_info()
    return Match(
        meta=meta,
        info=info,
        innings=[fake_innings(team) for team in info.teams],
    )


@pytest.fixture
def t20_match() -> Match:
    return Match(
        info=Info(),
        meta=Meta(),
        innings=[
            Innings(),
        ],
    )


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
