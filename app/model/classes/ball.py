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

    @property
    def outcome(self) -> int:
        if self.extra_type == "wide":
            return 0
        if self.extra_type == "noball":
            return 1
        if self.extra_type == "bye":
            return 2
        if self.extra_type == "legbye":
            return 3
        if self.wicket_fell:
            return 4
        if self.batter_runs == 0:
            return 5
        if self.batter_runs == 1:
            return 6
        if self.batter_runs == 2:
            return 7
        if self.batter_runs == 3:
            return 8
        if self.batter_runs == 4:
            return 9
        if self.batter_runs > 4:
            return 10
        return -1

    # endregion
