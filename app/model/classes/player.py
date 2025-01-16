from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from dataclasses_json import Undefined, dataclass_json

from app.model.classes.ball import Ball

AVG_RUNS_PER_BALL = 1.21
AVG_WICKET_PROB = 0.054


def empty_list(size: int) -> list[int]:
    return [0] * size


@dataclass
class BattingStat:
    balls_faced: int = 0
    times_out: int = 0
    runs_scored: int = 0


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
        if self.balls_bowled < 24 or self.wickets_taken < 1:
            return AVG_WICKET_PROB
        return float(self.wickets_taken) / self.balls_bowled

    def add(self, ball: Ball, batter: Player) -> None:
        self.balls_bowled += 1
        match ball.extra_type:
            case "bye", "legbye":
                pass
            case _:
                self.runs_conceded += ball.batter_runs
        if ball.wicket_fell and ball.how_out not in (
            "run out",
            "retired hurt",
            "retired not out",
            "retired out",
        ):
            self.wickets_taken += 1


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Player:
    player_id: int
    name: str
    bat_style: str = ""
    bowl_style: str = ""
    matches: int = 0
    # following are totals over *all* matches
    batting_positions: list[int] = field(default_factory=lambda: empty_list(11))
    balls_faced: int = 0
    times_out: int = 0
    scoring_shots: list[int] = field(default_factory=lambda: empty_list(7))
    overs_bowled: list[int] = field(default_factory=lambda: empty_list(20))
    # balls_bowled: int = 0
    noballs: int = 0
    wides: int = 0
    # runs_conceded: int = 0
    # wickets_taken: int = 0

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
        self.bowling_stats[batter.bat_style].add(ball, batter)
        self.bowling_stats["all"].add(ball, batter)

    def record_ball_faced(self, ball: Ball, bowler: Player) -> None:
        self.balls_faced += 1
        if ball.wicket_fell and ball.dismissed == self.name:
            self.times_out += 1
        elif not ball.wide_noball:
            self.scoring_shots[min(ball.batter_runs, 6)] += 1

    @property
    def total_runs_scored(self) -> int:
        return sum(shot_runs * times_recorded for shot_runs, times_recorded in enumerate(self.scoring_shots))

    @property
    def strike_rate(self) -> float:
        """
        runs per ball
        """
        return AVG_RUNS_PER_BALL if self.balls_faced < 10 else self.total_runs_scored / self.balls_faced

    @property
    def economy(self, bat_style: str = "all") -> float:
        """
        runs per ball
        """
        return self.bowling_stats[bat_style].economy

    @property
    def wicket_prob(self, bat_style: str = "all") -> float:
        """ "
        per ball
        """
        return self.bowling_stats[bat_style].wicket_prob

    @property
    def balls_bowled(self) -> int:
        return self.bowling_stats["all"].balls_bowled

    @property
    def runs_conceded(self) -> int:
        return self.bowling_stats["all"].runs_conceded

    @property
    def wide_rate(self) -> float:
        return 0.0 if self.balls_bowled == 0 else float(self.wides) / self.balls_bowled

    @property
    def noball_rate(self) -> float:
        return 0.0 if self.balls_bowled == 0 else float(self.noballs) / self.balls_bowled

    def __repr__(self) -> str:
        s = (
            f"{self.name=} {self.player_id=} {self.matches} apps,"
            f" bat:{self.bat_style} bowl:{self.bowl_style}"
            f" {self.total_runs_scored=} off {self.balls_faced=} {self.strike_rate=:0.2f}"
            f" {self.runs_conceded=} from {self.balls_bowled=} {self.economy=:0.2f}"
            f" w: {self.wide_rate:0.2f} nb: {self.noball_rate:0.2f}"
        )
        return s.replace("self.", "")

    # endregion
