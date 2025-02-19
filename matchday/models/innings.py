from dataclasses import dataclass, field

from matchday.models.ball import Ball
from matchday.models.player import Player
from matchday.models.team import Team


@dataclass
class Innings:
    batting: Team = field(default_factory=Team)
    bowling: Team = field(default_factory=Team)
    total: int = 0
    wickets: int = 0
    fours: int = 0
    sixes: int = 0
    closed: bool = False

    def __post_init__(self) -> None:
        for i, _ in enumerate(self.batting.players):
            setattr(self, f"batter_{i}", self.make_batter_lookup_func(i))

        for i, _ in enumerate(self.bowling.players):
            setattr(self, f"bowler_{i}", self.make_bowler_lookup_func(i))

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs + ball.penalty_runs
        if ball.wicket_fell:
            self.wickets += 1
        self.batting.update_batting(ball)
        self.bowling.update_bowling(ball)
        self.fours += 1 if ball.batter_runs == 4 else 0
        self.sixes += 1 if ball.batter_runs == 6 else 0

    @property
    def score(self) -> str:
        return f"{self.batting.name}: {self.total} - {self.wickets}"

    @property
    def boundaries(self) -> str:
        return f"{self.fours} four(s), {self.sixes} six(es)"

    def make_batter_lookup_func(self, index: int):
        def batter_lookup() -> Player:
            for p in self.batting.players.values():
                if p.bat_position == index:
                    return p
            return Player()

        return batter_lookup

    def make_bowler_lookup_func(self, index: int):
        def bowler_lookup() -> Player:
            for p in self.bowling.players.values():
                if p.bowl_position == index:
                    return p
            return Player()

        return bowler_lookup
