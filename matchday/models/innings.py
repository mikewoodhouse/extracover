from dataclasses import dataclass, field

from matchday.models.ball import Ball
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
