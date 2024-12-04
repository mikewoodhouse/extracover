from dataclasses import dataclass
from random import Random

from app.model.classes import Outcome

from .scorebook import Ball

# hard-code these for now - any situation-dependant variations are probably 2nd- or 3rd-order
# weights derived from all male T20 matches up to & including 2024-04-07

# try to deal with (not well identified) competitions where a no-ball costs 2: can spot them when
# there are batter runs but not entirely where the penalty was 1 and batters ran a bye. Anyway, close enough...
# with noballs AS (
# 	select CASE batter_runs WHEN 0 THEN extra_runs ELSE 1 END AS extras
# 	FROM balls WHERE extra_type = 'noball')
# select extras, count(*) from noballs group by extras order by extras
NB_EXTRA_RUNS: list[int] = [0, 6293, 972, 66, 87, 0, 38]

# select count(*) from balls where extra_type = 'noball' group by batter_runs order by batter_runs
NB_BATTER_RUNS: list[int] = [3500, 2039, 449, 19, 928, 0, 521]

# select count(*) from balls where extra_type = 'wide' group by batter_runs order by batter_runs
WIDE_EXTRA_RUNS: list[int] = [0, 50490, 2373, 505, 84, 1942]

# as for wides above
BYE_EXTRA_RUNS: list[int] = [0, 3722, 463, 61, 1438, 4]

# as for wides above
LEGBYE_EXTRA_RUNS: list[int] = [0, 23300, 1423, 128, 1901, 31, 1]


@dataclass
class BallParams:
    p_wide: float = 0.0
    p_noball: float = 0.0
    p_bye: float = 0.0
    p_legbye: float = 0.0
    p_wicket: float = 0.0
    p_dotball: float = 0.0
    p_single: float = 0.0
    p_two: float = 0.0
    p_three: float = 0.0
    p_four: float = 0.0
    p_six: float = 0.0

    @property
    def p_wnb(self) -> float:
        return self.p_wide + self.p_noball

    @property
    def probability_array(self) -> list[float]:
        return [
            self.p_wide,
            self.p_noball,
            self.p_bye,
            self.p_legbye,
            self.p_wicket,
            self.p_dotball,
            self.p_single,
            self.p_two,
            self.p_three,
            self.p_four,
            self.p_six,
        ]


class Balluator:
    def __init__(self, rnd: Random | None) -> None:
        self.rnd = rnd or Random()

    def result(self, params: BallParams) -> Ball:
        outcome = self.index_from(params.probability_array)
        match outcome:
            case Outcome.WIDE:
                extra_runs = self.index_from(WIDE_EXTRA_RUNS)
                return Ball(wide=True, extra_runs=extra_runs)
            case Outcome.NOBALL:
                extra_runs = self.index_from(NB_EXTRA_RUNS)
                batter_runs = self.index_from(NB_BATTER_RUNS)
                return Ball(noball=True, extra_runs=extra_runs, batter_runs=batter_runs)
            case Outcome.BYE:
                extra_runs = self.index_from(BYE_EXTRA_RUNS)
                return Ball(bye=True, extra_runs=extra_runs)
            case Outcome.LEGBYE:
                extra_runs = self.index_from(LEGBYE_EXTRA_RUNS)
                return Ball(legbye=True, extra_runs=extra_runs)
            case Outcome.WICKET:
                return Ball(wicket_fell=True)
            case Outcome.DOTBALL:
                return Ball()
            case Outcome.SINGLE:
                return Ball(batter_runs=1)
            case Outcome.TWO:
                return Ball(batter_runs=2)
            case Outcome.THREE:
                return Ball(batter_runs=3)
            case Outcome.FOUR:
                return Ball(batter_runs=4)
            case Outcome.SIX:
                return Ball(batter_runs=6)
            case _:
                raise ValueError(f"Unexpected {outcome=}")

    def index_from(self, weights: list[int] | list[float]) -> int:
        return self.rnd.choices(range(len(weights)), weights=weights, k=1)[0]
