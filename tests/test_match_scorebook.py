import sqlite3
from pathlib import Path

from app.model import Ball, Scorebook
from config import config

from .model.fakes import fake_book

SQL = """
SELECT
    batter_runs
,   extra_runs
,   wicket_fell
,   extra_type
FROM balls
WHERE match_id = 4095
ORDER BY innings, ball_seq
"""


def update_book(book: Scorebook, balls: list[Ball]) -> None:
    for ball in balls:
        book.update(ball)


def test_run_entire_match_ball_set_from_db():
    db_path = Path(__file__).parent.parent / config.db_filename
    print(db_path)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    balls = [Ball.from_db(dict(row)) for row in db.execute(SQL).fetchall()]
    assert len(balls) == 251
    book = fake_book()
    update_book(book, balls)
    assert book.first_innings.total - book.second_innings.total == 29
