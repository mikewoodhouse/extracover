from contextlib import nullcontext as does_not_raise

import pytest

from app.model.bowling_order_generator import (
    BowlingOrderGenerator,
    OverFrequencyRecord,
    OverWeightings,
)


@pytest.fixture
def bowler_over_freqs() -> list[OverWeightings]:
    return []


def test_raises_if_less_than_five_bowlers():
    with pytest.raises(ValueError, match="too few"):
        _ = BowlingOrderGenerator(
            [
                OverFrequencyRecord(name=str(i), over=o, frequency=0.05)
                for o in range(20)
                for i in range(4)
            ]
        )


def test_raises_if_any_overs_with_no_frequencies():
    with pytest.raises(ValueError, match="for at least"):
        _ = BowlingOrderGenerator([])
