from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from matchday.models.ball import Ball
from matchday.models.team import Team


@dataclass
class Book(DataClassJsonMixin):
    book_id: int = -1
    team_1: Team = field(default_factory=Team)
    team_2: Team = field(default_factory=Team)

    @property
    def batting(self) -> Team:
        return self.team_1

    @property
    def bowling(self) -> Team:
        return self.team_2

    def update(self, ball: Ball) -> None:
        pass
