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
    "p_wicket": 0.07,  # 0.18-0.25
    "p_dotball": 0.10,  # 0.25-0.35
    "p_single": 0.11,  # 0.35-0.46
    "p_two": 0.12,  # 0.46-0.58
    "p_three": 0.13,  # 0.58-0.71
    "p_four": 0.14,  # 0.71-0.85
    "p_six": 0.15,  # 0.85-1.00
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


@pytest.fixture
def ball_params() -> BallParams:
    return BallParams(**FAKE_PROBS)


# @pytest.mark.skip("")
@pytest.mark.parametrize(
    "rands,expected,desc",
    [
        ([0.01, 0.001], Ball(wide=True, extra_runs=1), "wide ball"),
        ([0.01, 0.9999], Ball(wide=True, extra_runs=5), "five wides"),
        ([0.05, 0.001, 0.001], Ball(noball=True, extra_runs=1), "nb"),
        ([0.05, 0.999, 0.0001], Ball(noball=True, extra_runs=6), "four noballs"),
        (
            [0.05, 0.001, 0.99],
            Ball(noball=True, extra_runs=1, batter_runs=6),
            "nb, batter hit 6",
        ),
        ([0.08, 0.001], Ball(bye=True, extra_runs=1), "bye"),
        ([0.13, 0.001], Ball(legbye=True, extra_runs=1), "legbye"),
        ([0.19], Ball(wicket_fell=True), "wicket!"),
        ([0.30], Ball(batter_runs=0), "dot-ball"),
        ([0.40], Ball(batter_runs=1), "single"),
        ([0.50], Ball(batter_runs=2), "two"),
        ([0.60], Ball(batter_runs=3), "three"),
        ([0.75], Ball(batter_runs=4), "four"),
        ([0.90], Ball(batter_runs=6), "six"),
    ],
)
def test_result(ball_params: BallParams, rands: list[float], expected: Ball, desc: str):
    rng = FakeRandom()
    rng.sequence = rands
    obj = Balluator(rng)
    assert obj.result(ball_params) == expected, desc


def test_probs_combined_in_correct_order():
    parms = BallParams(**FAKE_PROBS)
    assert sorted(FAKE_PROBS.values()) == parms.probability_array
