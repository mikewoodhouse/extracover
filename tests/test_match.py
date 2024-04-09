from datetime import date
from pathlib import Path

import pytest

from app.match import Match


@pytest.fixture
def m() -> Match:
    path = Path(__file__).with_name("1418196.json")
    assert path.exists()
    return Match.from_json(path.read_text())


def test_match_from_json_meta(m):
    assert m.meta.data_version == "1.1.0"
    assert m.meta.created == date(2024, 2, 14)
    assert m.meta.revision == 1


def test_match_from_json_info(m):
    i = m.info
    assert i.balls_per_over == 6
    assert i.city == "Bangkok"
    assert all(isinstance(dt, date) for dt in i.dates)
    assert len(i.dates) == 1
    assert i.dates[0] == date(2024, 2, 11)
    assert i.event.name == "Asian Cricket Council Men's Challenger Cup"
    assert i.event.stage == "3rd Place Play-Off"
    assert i.gender == "male"
    assert i.match_type == "T20"
    assert i.overs == 20
    assert len(i.teams) == 2
    assert all(t in i.teams for t in ["Japan", "Singapore"])
    assert i.toss.decision == "field"
    assert i.toss.winner == "Singapore"
    assert len(i.players) == 2
    assert all(len(player_list) == 11 for player_list in i.players.values())
    assert isinstance(i.registry.people, dict)
    assert all(
        nm in i.registry.people for nm in i.players["Japan"] + i.players["Singapore"]
    )
    assert i.venue == "Terdthai Cricket Ground, Bangkok"
