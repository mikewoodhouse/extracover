from dataclasses import dataclass
from enum import IntEnum
from random import Random

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


BYE_EXTRA_RUNS: list[int] = [0, 3722, 463, 61, 1438, 4]


LEGBYE_EXTRA_RUNS: list[int] = [0, 23300, 1423, 128, 1901, 31, 1]


class Outcome(IntEnum):
    WIDE = 0
    NOBALL = 1
    BYE = 2
    LEGBYE = 3
    WICKET = 4
    DOTBALL = 5
    SINGLE = 6
    TWO = 7
    THREE = 8
    FOUR = 9
    SIX = 10


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
        outcome = self.rnd.choices(
            range(len(params.probability_array)), weights=params.probability_array
        )[0]
        match outcome:
            case Outcome.WIDE:
                extra_runs = self.rnd.choices(
                    range(len(WIDE_EXTRA_RUNS)), weights=WIDE_EXTRA_RUNS, k=1
                )[0]
                return Ball(wide=True, extra_runs=extra_runs)
            case Outcome.NOBALL:
                extra_runs = self.rnd.choices(
                    range(len(NB_EXTRA_RUNS)), weights=NB_EXTRA_RUNS, k=1
                )[0]
                batter_runs = self.rnd.choices(
                    range(len(NB_BATTER_RUNS)), weights=NB_BATTER_RUNS, k=1
                )[0]
                return Ball(noball=True, extra_runs=extra_runs, batter_runs=batter_runs)
            case _:
                raise ValueError(f"Unexpected {outcome=}")
