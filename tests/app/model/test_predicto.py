import pytest

from app.model.predicto import Predicto
from app.model.scorebook import InningsCard, Match, Player, Scorebook

"""
# Setting up the model

For one simulation of a match we need to set up the Scorebook with
* Player info
    * historic stats as per the ML model
* Teams
    * 2 x Innings, with batting & bowling order

We also need:
* ML model

For multiple sims, we additionally need
* Extended Player info
    * historic batting position record for batting order generation
    * historic overs bowled record for bowling order generation
"""


def fake_match() -> Match:
    return Match()


def fake_first_innings() -> InningsCard:
    return InningsCard(batters=[Player(name=f"{i:02d}-Batter") for i in range(11)])


def fake_second_innings() -> InningsCard:
    return InningsCard(batters=[Player(name=f"{i:02d}-Batter") for i in range(11)])


@pytest.fixture
def fake_scorebook() -> Scorebook:
    return Scorebook(
        match=fake_match(),
        first_innings=fake_first_innings(),
        second_innings=fake_second_innings(),
    )


def test_it_builds(fake_scorebook):
    assert Predicto(fake_scorebook) is not None
