import random
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

import pytest

from app.ingest.classes import Event, Info, Innings, Match, Registry, Toss
from app.ingest.match_writer import MatchWriter
from app.utils import row_count


@pytest.fixture
def writer() -> MatchWriter:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    sql = Path(__file__).parent.parent / "schema.sql"
    with closing(db.cursor()) as csr:
        csr.executescript(sql.read_text())
    return MatchWriter(db)


@pytest.fixture
def info() -> Info:
    return Info(
        balls_per_over=6,
        toss=Toss(decision="field", winner="abc"),
        gender="male",
        match_type="T20",
        overs=20,
        venue="sidcup",
        dates=[
            date.today(),
        ],
        registry=Registry(),
        city="",
        event=Event(name="cup", stage="first"),
    )


def test_team_writing(writer: MatchWriter):  # sourcery skip: extract-duplicate-method
    teams_1 = ["abc", "def"]
    writer.write_teams(teams_1)
    assert len(writer.team_ids) == 2
    assert writer.team_ids["abc"] == 1
    teams_2 = ["abc", "ghi"]
    writer.write_teams(teams_2)
    assert len(writer.team_ids) == 3
    assert writer.team_ids["abc"] == 1


def test_info_writing(writer: MatchWriter, info: Info):
    assert writer.match_id < 0
    writer.write_match_from_info(info)
    assert writer.match_id > 0
    # TODO: check individual field content? Maybe later - match info not most important at this time


def test_player_selection_writing(writer: MatchWriter, info: Info):
    info.registry = Registry(
        people={
            "1a": "a",
            "1b": "b",
            "2c": "c",
            "2d": "d",
            "umpire": "e",
        }
    )
    info.players = {
        "1": ["1a", "1b"],
        "2": ["2c", "2d"],
    }
    match_id = random.randint(100, 200)
    writer.match_id = match_id
    writer.team_ids = {"1": 100, "2": 200}
    writer.write_player_selections(info)
    assert row_count(writer.db, "players") == 4
    assert row_count(writer.db, "selections") == 4


@pytest.mark.skip("needs player names, selections etc to be present in db")
@pytest.mark.usefixtures("fake_match")
def test_innings_writing(fake_match: Match, writer: MatchWriter):
    innings: Innings = fake_match.innings[0]
    ball_count = sum(len(over.deliveries) for over in innings.overs)
    assert ball_count > 0, "must be some balls in innings for test to be valid"
    writer.write_innings_deliveries(0, innings)
    writer.db.commit()
    assert row_count(writer.db, "balls") == ball_count
