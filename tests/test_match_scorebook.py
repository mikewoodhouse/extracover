import sqlite3
from pathlib import Path

import pytest

from app.config import config
from app.model import Ball, Player, Scorebook

from .model.fakes import fake_book

# USING match from 1422138.json

# There's an issue with the query plan referencing the all_balls view (~25sec)
# so use the query itself
#
# BALLS_SQL = """
# SELECT
#     b.striker_name
# ,   b.non_striker_name
# ,   b.bowler_name
# ,   b.batter_runs
# ,   b.extra_runs
# ,   b.wicket_fell
# ,   b.extra_type
# ,   b.seq
# FROM all_balls b
# JOIN matches m ON b.match_id = m.rowid
# WHERE m.file_path LIKE '%1422138%'
# ORDER BY b.seq
# """

BALLS_SQL = """
WITH
  the_match AS (
  SELECT rowid as match_id
  FROM matches m
  WHERE m.file_path LIKE '%1422138%'
)
,  sequenced_balls AS (
    SELECT
      innings * 10000 + over * 100 + ball_seq AS seq
    , *
    FROM
      balls
    WHERE innings < 2 /* in case there was a super over */
  )
SELECT
    b.batter_runs
,   b.extra_runs
,   b.wicket_fell
,   b.extra_type
,   b.seq
, strikers.name         AS striker_name
, non_strikers.name     AS non_striker_name
, bowlers.name          AS bowler_name
FROM
  sequenced_balls b
  JOIN players strikers ON strikers.rowid = b.batter
  JOIN players non_strikers ON non_strikers.rowid = b.non_striker
  JOIN players bowlers ON bowlers.rowid = b.bowled_by
  JOIN the_match m ON m.match_id = b.match_id
ORDER BY seq;
"""

book = fake_book()
book.first_innings.batters = [
    Player(name="RG Sharma"),
    Player(name="Ishan Kishan"),
    Player(name="SA Yadav"),
    Player(name="HH Pandya"),
    Player(name="Tilak Varma"),
    Player(name="TH David"),
    Player(name="R Shepherd"),
    Player(name="Mohammad Nabi"),
    Player(name="G Coetzee"),
    Player(name="PP Chawla"),
    Player(name="JJ Bumrah"),
]
book.second_innings.batters = [
    Player(name="PP Shaw"),
    Player(name="Tilak Varma"),
    Player(name="DA Warner"),
    Player(name="TH David"),
    Player(name="Abishek Porel"),
    Player(name="R Shepherd"),
    Player(name="T Stubbs"),
    Player(name="RR Pant"),
    Player(name="AR Patel"),
    Player(name="Lalit Yadav"),
    Player(name="Kumar Kushagra"),
    Player(name="JA Richardson"),
]


def update_book(book: Scorebook, rows: list[dict]) -> None:
    for row in rows:
        ball = Ball.from_db(row)
        book.update(ball)


@pytest.mark.skip()
def test_run_entire_match_ball_set_from_db():
    db_path = Path(__file__).parent.parent / config.db_filename
    print(db_path)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    balls = [dict(row) for row in db.execute(BALLS_SQL).fetchall()]

    assert len(balls) == 251

    update_book(book, balls)
    assert book.first_innings.total - book.second_innings.total == 29
    assert book.first_innings.wickets == 5
    assert book.second_innings.wickets == 8
    inns_1_scores = {
        batter.name: batter.runs_scored for batter in book.first_innings.batters
    }
    assert inns_1_scores["RG Sharma"] == 49
    assert inns_1_scores["Ishan Kishan"] == 42
    assert inns_1_scores["SA Yadav"] == 0
    assert inns_1_scores["HH Pandya"] == 39
    assert inns_1_scores["Tilak Varma"] == 6
    assert inns_1_scores["TH David"] == 45
    assert inns_1_scores["R Shepherd"] == 39
