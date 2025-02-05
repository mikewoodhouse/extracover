from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import DataClassJsonMixin


class Extra(StrEnum):
    NO_EXTRA = "None"
    WIDE = "w"
    NOBALL = "nb"
    BYE = "b"
    LEGBYE = "lb"


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

    @property
    def is_legal(self) -> bool:
        return self.extra_type not in [Extra.WIDE, Extra.NOBALL]

    @property
    def as_string(self) -> str:
        return str(self)

    @property
    def wicket_fell(self) -> bool:
        return self.striker_out or self.non_striker_out
