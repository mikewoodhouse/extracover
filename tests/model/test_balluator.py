from dataclasses import dataclass, field
from random import Random

import pytest

from app.model.balluator import BallParams, Balluator
from app.model.scorebook import Ball


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


@pytest.mark.parametrize(
    "parms,rands,expected,desc",
    [
        (BallParams(), [1.0], Ball(), "nothing happens"),
        (
            BallParams(p_noball=0.05),
            [
                0.01,
            ],
            Ball(noball=True),
            "nb",
        ),
        (
            BallParams(p_noball=0.05, p_wide=0.10),
            [
                0.07,
            ],
            Ball(wide=True),
            "wide",
        ),
    ],
)
def test_result(parms, rands, expected, desc):
    rng = FakeRandom()
    rng.sequence = rands
    obj = Balluator(rng)
    assert obj.result(parms) == expected, desc
