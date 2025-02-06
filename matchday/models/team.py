from __future__ import annotations

from dataclasses import asdict, dataclass, field

from app.config import config
from matchday.models.ball import Ball
from matchday.models.player import Player


@dataclass
class Team:
    name: str = ""
    players: dict[int, Player] = field(default_factory=dict)

    def update_batting(self, ball: Ball) -> None:
        self.players[ball.striker].update_as_striker(ball)
        self.players[ball.non_striker].update_as_non_striker(ball)

    def update_bowling(self, ball: Ball) -> None:
        self.players[ball.bowler].update_as_bowler(ball)

    @classmethod
    def all_as_dicts(cls) -> list[dict]:
        return [
            dict(row)
            for row in config.db_connection.execute(
                """
                SELECT * FROM teams ORDER BY name
                """
            ).fetchall()
        ]

    def players_as_dicts(self) -> list[dict]:
        all_players = Player.all_in_team(self.name)
        self.players = {p.player_id: p for p in all_players[:11]}  # TODO: handle changes to player selection
        return [asdict(p) for p in all_players]

    @property
    def batters(self) -> dict[int, str]:
        return {p.player_id: p.name for p in self.players.values() if not p.is_out}

    @property
    def bowlers(self) -> dict[int, str]:
        return {p.player_id: p.name for p in self.players.values() if not p.bowled_out}
