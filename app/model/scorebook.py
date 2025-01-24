from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from dataclasses_json import Undefined, dataclass_json

from app.model.batting_order_generator import BattingOrderGenerator
from app.model.bowling_order_generator import BowlingOrderGenerator


@dataclass
class Player:
    player_id: int = -1
    name: str = ""
    runs_scored: int = 0
    overs: int = 0
    runs_conceded: int = 0
    balls_faced: int = 0
    striker: bool = False
    non_striker: bool = False
    is_out: bool = False

    def out(self) -> None:
        self.is_out = True
        self.striker = False
        self.non_striker = False

    @property
    def batting_html(self) -> str:
        return (
            f"""<div style='display: flex; justify-content: space-between; width: 180px;'>"""
            f"""<div>{"*" if self.striker else ""}{"<b>" if self.striker or self.non_striker else ""}{self.name}</b></div>"""
            f"""<div>{self.runs_scored} ({self.balls_faced})</div>"""
        )


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


@dataclass_json(undefined=Undefined.EXCLUDE)
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
    extra_type: str = ""
    wide: bool = False
    noball: bool = False
    bye: bool = False
    legbye: bool = False
    penalty: bool = False

    def __post_init__(self):
        self.batter_runs = int(self.batter_runs)
        self.extra_runs = int(self.extra_runs)

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
        return (
            f"{self.striker_name}: {self.batter_runs}+{self.extra_runs}"
            f"{' *out* ' if self.wicket_fell else ' '}"
            f"{self.extra_type}"
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
    fours: int = 0
    sixes: int = 0

    def __post_init__(self) -> None:
        self.batters[0].striker = True
        self.batters[1].non_striker = True

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
        self.batters[self.striker_index].striker = True
        self.batters[self.striker_index].non_striker = False
        self.batters[self.non_striker_index].non_striker = True
        self.batters[self.non_striker_index].striker = False

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs
        self.striker.runs_scored += ball.batter_runs
        self.striker.balls_faced += 1

        if ball.batter_runs == 4:
            self.fours += 1

        if ball.batter_runs == 6:
            self.sixes += 1

        if ball.wicket_fell:
            self.wickets += 1
            if ball.striker_out:
                self.batters[self.striker_index].out()
                # TODO: at which end is the next man coming in?
            else:
                self.batters[self.non_striker_index].out()
                # TODO: at which end is the next man coming in?
            self.striker_index = self.next_man_in
            self.batters[self.striker_index].striker = True
            self.next_man_in += 1

        if ball.batter_runs in (1, 3):
            self.batsmen_change_ends()
        if ball.extra_runs in (2, 4):
            self.batsmen_change_ends()
        if ball.counts_toward_over:
            self.balls_bowled += 1
            if self.balls_bowled % 6 == 0:
                self.batsmen_change_ends()

    @property
    def score(self) -> str:
        return f"{self.total} - {self.wickets}"

    @property
    def rates(self) -> str:
        return f"ovs: {self.balls_bowled // 6}.{self.balls_bowled % 6} rr: {self.rpo:.2f}"

    @property
    def rpo(self) -> float:
        if self.balls_bowled == 0:
            return 0
        return self.total / self.balls_bowled * 6

    @property
    def boundaries(self) -> str:
        return f"{self.fours}x4 {self.sixes}x6"


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
