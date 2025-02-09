from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from dataclasses_json import Undefined, dataclass_json

from app.config import config
from matchday.common.db import sql
from matchday.models.ball import Ball


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Player:
    name: str = ""
    player_id: int = 0
    last_match: date = field(default=date.today())
    first_ball_recd: int = 0
    first_ball_bowled: int = 0

    bat_position: int = 0
    runs_scored: int = 0

    runs_conceded: int = 0
    wickets: int = 0

    bowl_position: int = 0
    balls_bowled: int = 0

    is_out: bool = False
    bowled_out: bool = False

    @staticmethod
    def all_in_team(name: str) -> list[Player]:
        with config.db_connection as conn:
            csr = conn.execute(
                sql("players_for_team"),
                {"team_name": name},
            )
            return [Player(**row) for row in csr.fetchall()]

    def update_as_striker(self, ball: Ball) -> None:
        self.runs_scored += ball.batter_runs
        self.is_out = ball.striker_out

    def update_as_non_striker(self, ball: Ball) -> None:
        self.is_out = ball.non_striker_out

    def update_as_bowler(self, ball: Ball) -> None:
        if ball.is_legal:
            self.balls_bowled += 1
        self.runs_conceded += ball.bowler_runs_conceded
        self.wickets += 1 if ball.wicket_credited_to_bowler else 0
