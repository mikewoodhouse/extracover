from dataclasses import dataclass, field
from random import Random

from .scorebook import Ball


@dataclass
class BallParams:
    p_noball: float = 0.0
    p_wide: float = 0.0
    p_wicket: float = 0.0
    p_nb_runs: list[float] = field(default_factory=list)
    p_wide_runs: list[float] = field(default_factory=list)
    p_runs: list[float] = field(default_factory=list)
    p_bye_runs: list[float] = field(default_factory=list)

    @property
    def p_wnb(self) -> float:
        return self.p_wide + self.p_noball


class Balluator:
    def __init__(self, rnd: Random | None) -> None:
        self.rnd = rnd or Random()

    def result(self, params: BallParams) -> Ball:
        r_wnb = self.rnd.random()
        if r_wnb <= params.p_wnb:
            return self.resolve_wnb(params, r_wnb)
        return Ball()

    def resolve_wnb(self, params: BallParams, r_wnb: float) -> Ball:
        if r_wnb < params.p_noball:
            return Ball(noball=True)
        return Ball(wide=True)
