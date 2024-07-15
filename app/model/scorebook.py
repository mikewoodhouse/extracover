from dataclasses import dataclass, field


@dataclass
class Ball:
    batter_runs: int = 0
    extra_runs: int = 0
    wicket_fell: bool = False
    striker_out: bool = True
    wide: bool = False
    noball: bool = False
    bye: bool = False

    @property
    def is_extra(self) -> bool:
        return self.wide or self.noball or self.bye

    @property
    def is_wide_no_ball(self) -> bool:
        return self.wide or self.noball

    @property
    def runs_scored(self) -> int:
        return self.batter_runs + self.extra_runs


@dataclass
class Player:
    name: str = ""
    runs_scored: int = 0
    overs: int = 0
    runs_conceded: int = 0


@dataclass
class Team:
    batting_order: list[Player] = field(default_factory=list)
    bowling_order: list[Player] = field(default_factory=list)


def int_list(size: int) -> list[int]:
    return [0] * size


@dataclass
class Scorebook:
    teams: list[Team] = field(default_factory=list)
    totals: list[int] = field(default_factory=list)
    batting_team: int = 0
    balls_bowled: int = 0

    def __post_init__(self) -> None:
        self.totals = int_list(2)

    def record_ball(self, ball: Ball) -> None:
        self.totals[self.batting_team] += ball.runs_scored
        if not ball.is_wide_no_ball:
            self.balls_bowled += 1
        if self.balls_bowled >= 120:
            self.close_first_innings()

    def close_first_innings(self) -> None:
        self.batting_team = 1
