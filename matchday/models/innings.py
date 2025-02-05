from dataclasses import dataclass, field

from matchday.models.team import Team


@dataclass
class Innings:
    batting: Team = field(default_factory=Team)
    bowling: Team = field(default_factory=Team)
    runs: int = 0
    wickets: int = 0
