import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from sidelined.over_rate_profile import OverRateProfile


@pytest.fixture
def db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    sql = Path(__file__).parent.parent.parent / "schema.sql"
    with closing(db.cursor()) as csr:
        csr.executescript(sql.read_text())

    for ov in range(20):
        db.execute(
            "INSERT INTO balls (innings, over, bowled_by, ball, batter_runs, extra_runs) VALUES (?, ?, ?, ?, ?, ?)",
            (0, ov, 0, 5, ov, 1),
        )

    db.commit()

    return db


def test_construction():
    pass


def test_diff():
    first = OverRateProfile(rates={i: 1.0 + i / 10 for i in range(20)})
    second = OverRateProfile(rates={i: 2.1 + i / 10 for i in range(20)})
    diff = second - first
    assert all(rt == pytest.approx(1.1) for rt in diff.rates.values())


def test_addition():
    first = OverRateProfile(rates={i: 1.0 + i / 10 for i in range(20)})
    second = OverRateProfile(rates={i: 2.1 + i / 10 for i in range(20)})
    diff = second + first
    expected_sum = OverRateProfile(rates={i: 3.1 + i * 2 / 10 for i in range(20)})
    assert all(
        actual == pytest.approx(expected)
        for actual, expected in zip(diff.rates.values(), expected_sum.rates.values())
    )


def test_getitem():
    obj = OverRateProfile(rates={i: i for i in range(20)})
    assert all(obj[i] == i for i in range(20))


def test_setitem():
    obj = OverRateProfile()
    # sourcery skip: no-loop-in-tests
    for i in range(20):
        obj[i] = i
    assert all(obj[i] == i for i in range(20))


def test_all_overs_construction(db):
    prof = OverRateProfile.by_all(db)
    assert all(prof[i] > 0 for i in range(20))


def test_by_bowler_construction(db):
    prof = OverRateProfile.by_bowler(db, 0)
    assert all(prof[i] > 0 for i in range(20))


def test_by_batter_construction(db):
    assert False
