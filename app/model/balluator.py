from dataclasses import dataclass, field
from random import Random

from .scorebook import Ball


@dataclass
class BallParams:
    p_wicket: float = 0.0
    p_wide: float = 0.0
    p_wide_runs: list[float] = field(default_factory=list)
    p_noball: float = 0.0
    p_nb_runs: list[float] = field(default_factory=list)
    p_bye_runs: list[float] = field(default_factory=list)
    p_runs: list[float] = field(default_factory=list)


class Balluator:
    def __init__(self, rnd: Random | None) -> None:
        self.rnd = rnd or Random()

    def result(self, params: BallParams) -> Ball:
        ball = Ball()
        if self.rnd.random() <= params.p_wicket:
            ball.wicket_fell = True

        return ball
