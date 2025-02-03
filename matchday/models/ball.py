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
    striker: int = -1
    non_striker: int = -1

    bowled_by: int = -1

    batter_runs: int = 0

    wicket_fell: bool = False

    extra_type: Extra = Extra.LEGAL_BALL
    extra_runs: int = 0

    penalty_runs: int = 0

    striker_out: bool = False
    non_striker_out: bool = False
