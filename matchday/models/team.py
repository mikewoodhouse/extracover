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
        striker = self.players[ball.striker]
        non_striker = self.players[ball.non_striker]
        if striker.bat_position == 0:
            striker.bat_position = 1 + max(p.bat_position for p in self.players.values())
        if non_striker.bat_position == 0:
            non_striker.bat_position = 1 + max(p.bat_position for p in self.players.values())
        striker.update_as_striker(ball)
        non_striker.update_as_non_striker(ball)

    def update_bowling(self, ball: Ball) -> None:
        for p in self.players.values():
            p.is_bowler = False
        bowler = self.players[ball.bowler]
        bowler.is_bowler = True
        if bowler.bowl_position == 0:
            bowler.bowl_position = 1 + max(p.bowl_position for p in self.players.values())
        bowler.update_as_bowler(ball)

    def switch_batters(self) -> None:
        striker = next(p for p in self.players.values() if p.is_striker)
        non_striker = next(p for p in self.players.values() if p.bat_position > 0 and not p.is_out and not p.is_striker)
        striker.is_striker = False
        non_striker.is_striker = True

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
