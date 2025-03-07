from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import DataClassJsonMixin


class Extra(StrEnum):
    NO_EXTRA = "None"
    WIDE = "w"
    NOBALL = "nb"
    BYE = "b"
    LEGBYE = "lb"


class HowOut(StrEnum):
    NOTOUT = "no"
    BOWLED = "b"
    CAUGHT = "c"
    LBW = "lbw"
    STUMPED = "st"
    RUN_OUT = "ro"
    OTHER = "other"


@dataclass
class Ball(DataClassJsonMixin):
    striker: int = -1
    non_striker: int = -1

    bowler: int = -1

    batter_runs: int = 0

    extra_type: Extra = Extra.NO_EXTRA
    extra_runs: int = 0

    penalty_runs: int = 0

    striker_out: bool = False
    non_striker_out: bool = False
    how_out: HowOut = HowOut.NOTOUT

    def reset(self) -> None:
        self.extra_type = Extra.NO_EXTRA
        self.batter_runs = self.extra_runs = self.penalty_runs = 0
        self.striker_out = False
        self.non_striker_out = False

    @property
    def bowler_runs_conceded(self) -> int:
        return self.batter_runs + (self.extra_runs if self.extra_type in [Extra.WIDE, Extra.NOBALL] else 0)

    @property
    def wicket_credited_to_bowler(self) -> bool:
        return self.how_out in [HowOut.BOWLED, HowOut.CAUGHT, HowOut.LBW, HowOut.STUMPED]

    @property
    def changes_ends(self) -> bool:
        if self.extra_type == Extra.NO_EXTRA:
            return self.batter_runs % 2 == 1
        if self.extra_type == Extra.BYE or self.extra_type == Extra.LEGBYE:
            return self.extra_runs % 2 == 1
        if self.extra_type == Extra.NOBALL:
            return self.batter_runs % 2 == 1 or (self.extra_runs - 1) % 2 == 1
        if self.extra_type == Extra.WIDE:
            # doesn't handle all cases, like all-run four off a wide, or boundary?
            return (self.extra_runs - 1) % 2 == 1
        return False

    @property
    def is_legal(self) -> bool:
        return self.extra_type not in [Extra.WIDE, Extra.NOBALL]

    @property
    def as_string(self) -> str:
        return str(self)

    @property
    def wicket_fell(self) -> bool:
        return self.striker_out or self.non_striker_out
