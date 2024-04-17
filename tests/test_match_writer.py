import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

import pytest

from app.ingest.classes import Event, Info, Registry, Toss
from app.ingest.match_writer import MatchWriter


@pytest.fixture
def db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    sql = Path(__file__).parent.parent / "schema.sql"
    with closing(db.cursor()) as csr:
        csr.executescript(sql.read_text())
    return db


def test_team_writing(db):
    writer = MatchWriter(db)
    teams_1 = ["abc", "def"]
    writer.write_teams(teams_1)
    assert len(writer.team_ids) == 2
    assert writer.team_ids["abc"] == 1
    teams_2 = ["abc", "ghi"]
    writer.write_teams(teams_2)
    assert len(writer.team_ids) == 3
    assert writer.team_ids["abc"] == 1


def test_info_writing(db):
    info = Info(
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
    writer = MatchWriter(db)
    assert writer.match_id < 0
    writer.write_match_info(info)
    assert writer.match_id > 0
    # CREATE TABLE IF NOT EXISTS
    #   matches (
    #     match_id INTEGER NOT NULL PRIMARY KEY
    #   , start_date DATE
    #   , match_type TEXT
    #   , gender TEXT
    #   , venue TEXT
    #   , event TEXT
    #   , city TEXT
    #   , overs INTEGER /* because the Hundred */
    #   , balls_per_over INTEGER /* because the Hundred */
    #   );
