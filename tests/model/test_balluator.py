from dataclasses import dataclass, field
from random import Random

import pytest

from app.model.balluator import BallParams, Balluator
from app.model.scorebook import Ball

FAKE_PROBS = {
    "p_wide": 0.03,
    "p_noball": 0.04,
    "p_bye": 0.05,
    "p_legbye": 0.06,
    "p_wicket": 0.07,
    "p_dotball": 0.10,
    "p_single": 0.11,
    "p_two": 0.12,
    "p_three": 0.13,
    "p_four": 0.14,
    "p_six": 0.15,
}


@dataclass
class FakeRandom(Random):
    sequence: list[float] = field(default_factory=list)
    idx: int = 0

    def random(self) -> float:
        next_val = self.sequence[self.idx]
        self.idx += 1
        return next_val


def test_creation():
    rng = FakeRandom()
    assert Balluator(rng)


# @pytest.mark.skip("")
@pytest.mark.parametrize(
    "parms,rands,expected,desc",
    [
        (
            BallParams(**FAKE_PROBS),
            [0.01, 0.001],
            Ball(wide=True, extra_runs=1),
            "wide",
        ),
        (
            BallParams(**FAKE_PROBS),
            [0.05, 0.001, 0.001],
            Ball(noball=True, extra_runs=1),
            "nb",
        ),
    ],
)
def test_result(parms: BallParams, rands: list[float], expected: Ball, desc: str):
    rng = FakeRandom()
    rng.sequence = rands
    obj = Balluator(rng)
    assert obj.result(parms) == expected, desc


def test_probs_combined_in_correct_order():
    parms = BallParams(**FAKE_PROBS)
    assert sorted(FAKE_PROBS.values()) == parms.probability_array
