# from contextlib import nullcontext as does_not_raise

import pytest

from app.model.bowling_order_generator import (
    BowlingOrderGenerator,
    OverFrequencyRecord,
    OverWeightings,
)


@pytest.fixture
def bowler_over_freqs() -> list[OverFrequencyRecord]:
    return [
        OverFrequencyRecord(name=str(i), player_id=i, over=o, frequency=1)
        for o in range(20)
        for i in range(5)
    ]


def test_raises_if_less_than_five_bowlers(bowler_over_freqs):
    four_bowler_version = list(
        filter(lambda f: f.name != "4", bowler_over_freqs)
    )  # remove bowler "4"
    with pytest.raises(ValueError, match="too few"):
        _ = BowlingOrderGenerator(four_bowler_version)


def test_raises_if_any_overs_with_no_frequencies():
    with pytest.raises(ValueError, match="for at least"):
        _ = BowlingOrderGenerator([])


def test_generates_a_valid_bowling_order(bowler_over_freqs):
    gen = BowlingOrderGenerator(bowler_over_freqs)
    order = gen.bowling_order()

    assert len(order) == 20


class TestOverWeightings:
    def test_selection(self):
        obj = OverWeightings(bowlers={100: 1, 101: 1})
        assert obj.selected([]) in [100, 101]
