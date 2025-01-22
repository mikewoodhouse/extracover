from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.model.batting_order_generator import BattingOrderGenerator
from app.model.bowling_order_generator import BowlingOrderGenerator


@dataclass
class Player:
    player_id: int = -1
    name: str = ""
    runs_scored: int = 0
    overs: int = 0
    runs_conceded: int = 0


@dataclass
class Team:
    name: str = ""
    players: list[Player] = field(default_factory=list)
    bowling_order_gen: BowlingOrderGenerator | None = None
    batting_order_gen: BattingOrderGenerator | None = None


@dataclass
class Match:
    match_id: int = 0
    start_date: date = field(default_factory=lambda: date.today())
    match_type: str = "T20"  # may want to become an enum?
    gender: str = "male"  # enum?
    venue: str = ""
    event: str = ""  # might want to become a foreign key to a future events table?
    city: str = ""
    overs: int = 20
    balls_per_over: int = 6
    teams: list[Team] = field(default_factory=list)
    bat_first: int = 0

    @property
    def db_params(self) -> dict:
        return {
            "start_date": self.start_date,
        }


@dataclass
class Ball:
    striker_name: str = ""
    non_striker_name: str = ""
    bowler_name: str = ""
    batter_runs: int = 0
    extra_runs: int = 0
    wicket_fell: bool = False
    striker_out: bool = True
    # TODO: would an "ExtraType" Enum be better?
    wide: bool = False
    noball: bool = False
    bye: bool = False
    legbye: bool = False
    penalty: bool = False

    @property
    def is_extra(self) -> bool:
        return self.wide or self.noball or self.bye

    @property
    def counts_toward_over(self) -> bool:
        return not (self.wide or self.noball)

    @property
    def runs_scored(self) -> int:
        return self.batter_runs + self.extra_runs

    def __str__(self) -> str:
        extra_type = "wide" if self.wide else ""
        extra_type = "noball" if self.noball else ""
        extra_type = "bye" if self.bye else ""
        extra_type = "legbye" if self.legbye else ""
        extra_type = "penalty" if self.penalty else ""

        return (
            f"{self.striker_name}: {self.batter_runs}+{self.extra_runs}"
            f"{' *out* ' if self.wicket_fell else ' '}"
            f"{extra_type}"
        )

    @classmethod
    def from_db(cls, row: dict) -> Ball:
        if extra_type := row.pop("extra_type", None):
            row[extra_type] = True
        row.pop("seq", None)

        return cls(**row)


@dataclass
class InningsCard:
    batters: list[Player] = field(default_factory=list)
    bowlers: list[Player] = field(default_factory=list)
    total: int = 0
    wickets: int = 0
    balls_bowled: int = 0
    striker_index: int = 0
    non_striker_index: int = 1
    next_man_in: int = 2

    @property
    def closed(self) -> bool:
        return self.balls_bowled >= 120 or self.wickets >= 10

    @property
    def striker(self) -> Player:
        return self.batters[self.striker_index]

    @property
    def non_striker(self) -> Player:
        return self.batters[self.non_striker_index]

    def batsmen_change_ends(self) -> None:
        self.striker_index, self.non_striker_index = (
            self.non_striker_index,
            self.striker_index,
        )

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs
        self.striker.runs_scored += ball.batter_runs
        if ball.wicket_fell:
            self.wickets += 1
            self.striker_index = self.next_man_in
            self.next_man_in += 1
        if ball.batter_runs in (1, 3):
            self.batsmen_change_ends()
        if ball.extra_runs in (2, 4):
            self.batsmen_change_ends()
        if ball.counts_toward_over:
            self.balls_bowled += 1
            if self.balls_bowled % 6 == 0:
                self.batsmen_change_ends()


@dataclass
class Scorebook:
    match: Match = field(default_factory=Match)  # type: ignore
    first_innings: InningsCard = field(default_factory=InningsCard)
    second_innings: InningsCard = field(default_factory=InningsCard)

    @property
    def current_innings(self) -> InningsCard:
        return self.second_innings if self.first_innings.closed else self.first_innings

    def update(self, ball: Ball) -> None:
        self.current_innings.update(ball)
