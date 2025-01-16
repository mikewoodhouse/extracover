from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from dataclasses_json import Undefined, dataclass_json

from app.model.classes.ball import Ball

AVG_RUNS_PER_BALL = 1.21
AVG_WICKET_PROB = 0.054
MIN_BALLS_FOR_WICKET_PROB: int = 24
MIN_BALLS_FOR_BATTER_DISMISSAL_PROB: int = 20


def empty_list(size: int) -> list[int]:
    return [0] * size


@dataclass
class BattingStat:
    balls_faced: int = 0
    times_out: int = 0
    runs_scored: int = 0

    def add(self, ball: Ball, name: str) -> None:
        self.balls_faced += 1
        if ball.wicket_fell and ball.dismissed == name:
            self.times_out += 1
        self.runs_scored += ball.batter_runs

    @property
    def strike_rate(self) -> float:
        return AVG_RUNS_PER_BALL if self.balls_faced < 10 else float(self.runs_scored) / self.balls_faced

    @property
    def dismissal_prob(self) -> float:
        return (
            AVG_WICKET_PROB
            if self.balls_faced < MIN_BALLS_FOR_BATTER_DISMISSAL_PROB
            else float(self.times_out) / self.balls_faced
        )

    def __repr__(self) -> str:
        return f"b={self.balls_faced} r={self.runs_scored} ({self.strike_rate:.1f}) w={self.times_out} ({self.dismissal_prob:.2%})"


@dataclass
class BowlingStat:
    balls_bowled: int = 0
    runs_conceded: int = 0
    wickets_taken: int = 0

    @property
    def economy(self) -> float:
        if self.balls_bowled < 12:
            return AVG_RUNS_PER_BALL
        return float(self.runs_conceded) / self.balls_bowled

    @property
    def wicket_prob(self) -> float:
        if self.balls_bowled < MIN_BALLS_FOR_WICKET_PROB or self.wickets_taken < 1:
            return AVG_WICKET_PROB
        return float(self.wickets_taken) / self.balls_bowled

    def add(self, ball: Ball, batter: Player) -> None:
        self.balls_bowled += 1
        match ball.extra_type:
            case "bye", "legbye":
                pass
            case _:
                # TODO: does using extras here have a risk of counting them twice somehow?
                self.runs_conceded += ball.batter_runs + ball.extra_runs
        if ball.wicket_fell and ball.how_out not in (
            "run out",
            "retired hurt",
            "retired not out",
            "retired out",
        ):
            self.wickets_taken += 1

    def __repr__(self) -> str:
        return f"b={self.balls_bowled} c={self.runs_conceded} ({self.economy:.1f}) w={self.wickets_taken} ({self.wicket_prob:.2%})"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Player:
    player_id: int
    name: str
    bat_style: str = ""
    bowl_style: str = ""
    matches: int = 0
    batting_positions: list[int] = field(default_factory=lambda: empty_list(11))
    scoring_shots: list[int] = field(default_factory=lambda: empty_list(7))
    overs_bowled: list[int] = field(default_factory=lambda: empty_list(20))
    noballs: int = 0
    wides: int = 0

    bowling_stats: dict[str, BowlingStat] = field(default_factory=lambda: defaultdict(BowlingStat))
    batting_stats: dict[str, BattingStat] = field(default_factory=lambda: defaultdict(BattingStat))

    # region methods

    def record_batting_position(self, pos: int) -> None:
        pos = min(pos, 10)  # b/c some leagues allow an injury substitute, BPL 2021/22 as an example
        self.batting_positions[pos] += 1

    def record_ball_bowled(self, ball: Ball, batter: Player) -> None:
        if ball.ball_seq == 0:
            self.overs_bowled[ball.over] += 1
        match ball.extra_type:
            case "wide":
                self.wides += 1
            case "noball":
                self.noballs += 1
            case _:
                pass
        self.bowling_stats[batter.bat_style or "r"].add(ball, batter)
        self.bowling_stats["all"].add(ball, batter)

    def record_ball_faced(self, ball: Ball, bowler: Player) -> None:
        self.batting_stats[bowler.bowl_style or "rf"].add(ball, self.name)
        self.batting_stats["all"].add(ball, self.name)
        if not ball.wide_noball:
            self.scoring_shots[min(ball.batter_runs, 6)] += 1

    def runs_scored(self, bowl_style: str = "all") -> int:
        return self.batting_stats[bowl_style].runs_scored

    def balls_faced(self, bowl_style: str = "all") -> int:
        return self.batting_stats[bowl_style].balls_faced

    def strike_rate(self, bowl_style: str = "all") -> float:
        return self.batting_stats[bowl_style].strike_rate

    def dismissal_prob(self, bowl_style: str = "all") -> float:
        vs_all = self.batting_stats["all"].dismissal_prob
        if bowl_style == "all":
            return vs_all
        if self.batting_stats[bowl_style].balls_faced < MIN_BALLS_FOR_BATTER_DISMISSAL_PROB:
            return vs_all
        return self.batting_stats[bowl_style].dismissal_prob

    def economy(self, bat_style: str = "all") -> float:
        return self.bowling_stats[bat_style].economy

    def wicket_prob(self, bat_style: str = "all") -> float:
        vs_all = self.bowling_stats["all"].wicket_prob
        if bat_style == "all":
            return vs_all
        if self.bowling_stats[bat_style].balls_bowled < MIN_BALLS_FOR_WICKET_PROB:
            return vs_all
        return self.bowling_stats[bat_style].wicket_prob

    def balls_bowled(self, bat_style: str = "all") -> int:
        return self.bowling_stats[bat_style].balls_bowled

    def runs_conceded(self, bat_style: str = "all") -> int:
        return self.bowling_stats[bat_style].runs_conceded

    @property
    def wide_rate(self) -> float:
        return 0.0 if self.balls_bowled == 0 else float(self.wides) / self.balls_bowled()

    @property
    def noball_rate(self) -> float:
        return 0.0 if self.balls_bowled == 0 else float(self.noballs) / self.balls_bowled()

    def __repr__(self) -> str:
        s = (
            f"{self.name=} {self.player_id=} {self.matches} apps,"
            f" bat:{self.bat_style} bowl:{self.bowl_style}"
            f" {self.runs_scored=} off {self.balls_faced()=} {self.strike_rate()=:0.2f}"
            f" {self.runs_conceded()=} from {self.balls_bowled()=} {self.economy()=:0.2f}"
            f" w: {self.wide_rate:0.2f} nb: {self.noball_rate:0.2f}"
        )
        return s.replace("self.", "")

    # endregion
