from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.config import config
from matchday.common.db import sql


@dataclass
class Player:
    name: str = ""
    player_id: int = 0
    last_match: date = field(default=date.today())
    first_ball_recd: int = 0
    first_ball_bowled: int = 0

    is_out: bool = False

    @staticmethod
    def all_in_team(name: str) -> list[Player]:
        with config.db_connection as conn:
            csr = conn.execute(
                sql("players_for_team"),
                {"team_name": name},
            )
            return [Player(**row) for row in csr.fetchall()]
