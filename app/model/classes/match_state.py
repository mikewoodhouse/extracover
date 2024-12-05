from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date

from app.model.classes.ball import Ball


@dataclass
class MatchState:
    match_number: int
    start_date: date
    innings: int = 0
    total: int = 0
    target: int = 0
    wickets: int = 0
    balls_bowled: int = 0
    run_rate: float = 0.0  # per *ball*
    req_rate: float = 0.0  # per *ball*
    batter: int = -1
    bowler: int = -1
    balls_faced: defaultdict[int, int] = field(default_factory=lambda: defaultdict(int))

    # region methods

    def update(self, ball: Ball) -> None:
        self.batter = ball.batter
        self.bowler = ball.bowled_by
        self.total += ball.batter_runs + ball.extra_runs
        if ball.batsman_out:
            self.wickets += 1
        if ball.was_legal:
            self.balls_bowled += 1
        self.run_rate = (
            float(self.total) / self.balls_bowled if self.balls_bowled else 0.0
        )
        self.balls_faced[ball.batter] += 1
        if ball.innings == 1:
            self.req_rate = (
                (self.target - self.total + 1.0) / (120.0 - self.balls_bowled)
                if self.balls_bowled < 120
                else 0.0
            )

    def __repr__(self) -> str:
        return f"{self.target=} {self.total=}/{self.wickets} {self.balls_bowled} {self.req_rate=}"

    # endregion
