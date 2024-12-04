from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Ball:
    innings: int
    over: int
    ball: int
    ball_seq: int

    batter: int
    non_striker: int
    bowled_by: int

    batter_runs: int
    extra_runs: int

    wicket_fell: bool

    extra_type: str

    dismissed: str
    how_out: str

    # region methods

    @property
    def wide_noball(self) -> bool:
        return self.extra_type in ("wide", "noball")

    @property
    def batsman_out(self) -> bool:
        return bool(self.how_out) and not self.how_out.startswith("retired")

    @property
    def was_legal(self) -> bool:
        return self.extra_type == ""

    # endregion
