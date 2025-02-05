from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from matchday.models.ball import Ball
from matchday.models.innings import Innings
from matchday.models.team import Team


@dataclass
class Book(DataClassJsonMixin):
    book_id: int = -1

    team_1: str = ""
    team_2: str = ""

    inns_1: Innings = field(default_factory=Innings)
    inns_2: Innings = field(default_factory=Innings)

    def __post_init__(self) -> None:
        self.current_innings = self.inns_1

    def innings_closed(self) -> None:
        self.current_innings = self.inns_2

    @property
    def batting(self) -> Team:
        return self.current_innings.batting

    @property
    def bowling(self) -> Team:
        return self.current_innings.bowling

    def update(self, ball: Ball) -> None:
        pass

    @property
    def score(self) -> str:
        def inns_score(name: str, inns: Innings) -> str:
            return f"{name}: {inns.total} - {inns.wickets}"

        return inns_score(self.team_1, self.inns_1) + (
            "" if self.current_innings == self.inns_1 else "\n" + inns_score(self.team_2, self.inns_2)
        )
