from datetime import date

import pytest

from app.ingest.classes import Event, Info, Match, Meta, Registry


@pytest.fixture
def info() -> Info:
    return Info(
        dates=[date.today()],
        balls_per_over=5,
        gender="unknown",
        match_type="banana",
        overs=42,
        venue="bolton",
        event=Event(name="the cup", stage="first"),
        city="apple",
    )


def test_info_database_fields(info):
    match = Match(
        meta=Meta(),
        info=info,
    )
    expected = {
        "start_date": date.today().isoformat(),
        "match_type": "banana",
        "gender": "unknown",
        "venue": "bolton",
        "event": "the cup|first",
        "city": "apple",
        "overs": 42,
        "balls_per_over": 5,
        "file_path": "",
    }
    assert match.info.database_fields() == expected


def test_repr(info):
    s = f"{info}"
    assert s[:4].isnumeric()


def test_selected_player_regs(info: Info):
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
    assert len(info.selected_player_regs) == 4
    assert all(len(item) == 3 for item in info.selected_player_regs)
    expected_keys = sorted(["name", "reg", "team"])
    assert all(
        sorted(item.keys()) == expected_keys for item in info.selected_player_regs
    )
