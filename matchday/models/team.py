from __future__ import annotations

from dataclasses import asdict, dataclass, field

from app.config import config
from matchday.models.player import Player


@dataclass
class Team:
    name: str = ""
    players: list[Player] = field(default_factory=list)

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
        self.players = Player.all_in_team(self.name)
        return [asdict(p) for p in self.players]
