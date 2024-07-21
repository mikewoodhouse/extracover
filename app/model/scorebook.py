from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Ball:
    striker_name: str = ""
    non_striker_name: str = ""
    bowler_name: str = ""
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
    def counts_toward_over(self) -> bool:
        return not (self.wide or self.noball)

    @property
    def runs_scored(self) -> int:
        return self.batter_runs + self.extra_runs

    def __str__(self) -> str:
        extra_type = "wide" if self.wide else ""
        extra_type = "noball" if self.noball else ""
        extra_type = "bye" if self.bye else ""

        return (
            f"{self.striker_name}: {self.batter_runs}+{self.extra_runs}"
            f"{' *out* ' if self.wicket_fell else ' '}"
            f"{extra_type}"
        )

    @classmethod
    def from_db(cls, row: dict) -> Ball:
        match row["extra_type"]:
            case "wide":
                row["wide"] = True
            case "noball":
                row["noball"] = True
            case "bye":
                row["bye"] = True
            case "legbye":
                row["bye"] = True
            case _:
                pass
        row.pop("extra_type")

        return cls(**row)


@dataclass
class Player:
    name: str = ""
    runs_scored: int = 0
    overs: int = 0
    runs_conceded: int = 0


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
    first_innings: InningsCard = field(default_factory=InningsCard)
    second_innings: InningsCard = field(default_factory=InningsCard)

    @property
    def current_innings(self) -> InningsCard:
        return self.second_innings if self.first_innings.closed else self.first_innings

    def update(self, ball: Ball) -> None:
        self.current_innings.update(ball)
