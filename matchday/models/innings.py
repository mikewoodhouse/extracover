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

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs + ball.penalty_runs
        if ball.wicket_fell:
            self.wickets += 1
        self.batting.update_batting(ball)
        self.bowling.update_bowling(ball)

    def __post_init__(self) -> None:
        for i, _ in enumerate(self.batting.players):
            setattr(self, f"batter_{i}", self.make_batter_lookup_func(i))

        for i, _ in enumerate(self.bowling.players):
            setattr(self, f"bowler_{i}", self.make_bowler_lookup_func(i))

    def make_batter_lookup_func(self, index: int):
        def batter_lookup() -> Player:
            for p in self.batting.players.values():
                if p.bat_position == index:
                    return p
            return Player()

        return batter_lookup

    def make_bowler_lookup_func(self, index: int):
        def bowler_lookup() -> Player:
            return next(p for p in self.bowling.players.values() if p.bowl_position == index)

        return bowler_lookup
