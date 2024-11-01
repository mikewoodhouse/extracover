from dataclasses import dataclass, field
from random import Random

import pytest

from app.model.balluator import BallParams, Balluator
from app.model.scorebook import Ball


@dataclass
class NotRandom(Random):
    sequence: list[float] = field(default_factory=list)
    idx: int = 0

    def random(self) -> float:
        next_val = self.sequence[self.idx]
        self.idx += 1
        return next_val


def test_creation():
    rng = NotRandom()
    assert Balluator(rng)


@pytest.mark.parametrize(
    "parms,expected,rands,desc",
    [
        (BallParams(), Ball(), [1.0], "nothing happens"),
        (
            BallParams(p_wicket=0.05),
            Ball(wicket_fell=True),
            [
                0.01,
            ],
            "wicket",
        ),
    ],
)
def test_result(parms, expected, rands, desc):
    rng = NotRandom()
    rng.sequence = rands
    obj = Balluator(rng)
    assert obj.result(parms) == expected, desc
