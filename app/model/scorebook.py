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
    def counts_toward_over(self) -> bool:
        return not (self.wide or self.noball)

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
class InningsCard:
    batters: list[Player] = field(default_factory=list)
    bowlers: list[Player] = field(default_factory=list)
    total: int = 0
    wickets: int = 0
    balls_bowled: int = 0
    striker_index: int = 0
    non_striker_index: int = 1

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
        if ball.batter_runs in (1, 3):
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
