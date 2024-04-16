from datetime import date
from pathlib import Path

import pytest

from app.ingest.classes import Delivery, Match, PowerPlay


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


def test_match_from_json_innings(m):
    i = m.innings
    assert len(i) == 2
    assert i[0].team == "Japan"
    assert i[1].team == "Singapore"
    inn_0 = i[0]
    assert len(inn_0.overs) == 20
    d = inn_0.overs[0].deliveries[0]
    assert d.extras.noballs == 1
    assert all(isinstance(inns.powerplays, list) for inns in i)
    assert all(isinstance(pp, PowerPlay) for inns in i for pp in inns.powerplays)
    assert i[0].target.overs == 0
    assert i[1].target.overs == 20


def test_match_from_json_no_wicket(m):
    i = m.innings
    inns = i[0]
    wkt_ball = inns.overs[0].deliveries[1]
    assert len(wkt_ball.wickets) == 0


def test_match_from_json_wicket_fell(m):
    i = m.innings
    inns = i[0]
    wkt_ball = inns.overs[0].deliveries[2]
    assert len(wkt_ball.wickets) == 1
    wkt = wkt_ball.wickets[0]
    assert wkt.player_out == "L Yamamoto-Lake"
    assert wkt.kind == "caught"


def test_wickets_at_start_of_over(m):
    inns = m.innings[0]
    assert inns.overs[0].wickets_down_at_start == 0
    assert inns.overs[1].wickets_down_at_start == 1
    assert inns.overs[13].wickets_down_at_start == 2


def test_delivery_import_with_no_extras():
    d = """{
              "batter": "K Kadowaki-Fleming",
              "bowler": "R Kalimuthu",
              "non_striker": "L Yamamoto-Lake",
              "runs": {
                "batter": 1,
                "extras": 0,
                "total": 1
              }
            }"""
    deliv = Delivery.from_json(d)
    assert deliv.runs.total == 1
    assert deliv.extras.noballs == 0


def test_delivery_import_with_extras():
    d = """{
              "batter": "K Kadowaki-Fleming",
              "bowler": "R Kalimuthu",
              "extras": {
                "noballs": 1
              },
              "non_striker": "L Yamamoto-Lake",
              "runs": {
                "batter": 1,
                "extras": 1,
                "total": 2
              }
            }"""
    deliv = Delivery.from_json(d)
    assert deliv.runs.total == 2
    assert deliv.extras.noballs == 1
