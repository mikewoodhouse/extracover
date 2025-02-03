from dataclasses import dataclass
from enum import StrEnum

from dataclasses_json import DataClassJsonMixin


class Extra(StrEnum):
    LEGAL_BALL = "None"
    WIDE = "w"
    NOBALL = "nb"
    BYE = "b"
    LEGBYE = "lb"


@dataclass
class Ball(DataClassJsonMixin):
    striker: int
    non_striker: int

    bowled_by: int

    batter_runs: int

    wicket_fell: bool

    extra_type: Extra
    extra_runs: int

    penalty_runs: int

    striker_out: bool = False
    non_striker_out: bool = False
