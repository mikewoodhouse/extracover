from dataclasses import dataclass, field
from datetime import date

from dataclasses_json import DataClassJsonMixin, config, dataclass_json


def date_field():
    return field(metadata=config(encoder=date.isoformat, decoder=date.fromisoformat))


def date_list_decoder(dts: list[str]) -> list[date]:
    return [date.fromisoformat(s) for s in dts]


@dataclass_json
@dataclass
class Meta:
    data_version: str
    revision: int
    created: date = date_field()


@dataclass_json
@dataclass
class Event:
    name: str
    stage: str


@dataclass_json
@dataclass
class Toss:
    decision: str
    winner: str


@dataclass_json
@dataclass
class Registry:
    people: dict[str, str] = field(default_factory=dict)


@dataclass_json
@dataclass
class Info:
    balls_per_over: int
    city: str
    event: Event
    toss: Toss
    gender: str
    match_type: str
    overs: int
    venue: str
    dates: list[date] = field(metadata=config(decoder=date_list_decoder))
    registry: Registry
    players: dict[str, list[str]] = field(default_factory=dict)
    teams: list[str] = field(default_factory=list)


@dataclass_json
@dataclass
class Extras:
    noballs: int = 0
    wides: int = 0
    legbyes: int = 0
    byes: int = 0


@dataclass_json
@dataclass
class Runs:
    batter: int = 0
    extras: int = 0
    total: int = 0


@dataclass_json
@dataclass
class Dismissal:
    player_out: str
    kind: str


@dataclass
class Delivery(DataClassJsonMixin):
    batter: str = ""
    bowler: str = ""
    non_striker: str = ""
    runs: Runs = field(default_factory=Runs)
    extras: Extras = field(default_factory=Extras)
    wickets: list[Dismissal] = field(default_factory=list)


@dataclass_json
@dataclass
class Over:
    over: int
    deliveries: list[Delivery] = field(default_factory=list)

    @property
    def runs(self) -> int:
        return sum(deliv.runs.total for deliv in self.deliveries)


@dataclass_json
@dataclass
class PowerPlay:
    type: str
    ball_from: float = field(metadata=config(field_name="from"))
    ball_to: float = field(metadata=config(field_name="to"))

    @property
    def first_over(self) -> int:
        return int(self.ball_from)

    @property
    def last_over(self) -> int:
        return int(self.ball_to)

    @property
    def overs(self) -> range:
        return range(self.first_over, self.last_over + 1)


@dataclass_json
@dataclass
class Target:
    overs: int = 0
    runs: int = 0


@dataclass_json
@dataclass
class Innings:
    team: str
    overs: list[Over] = field(default_factory=list)
    powerplays: list[PowerPlay] = field(default_factory=list)
    target: Target = field(default_factory=Target)


@dataclass
class Match(DataClassJsonMixin):
    meta: Meta
    info: Info
    innings: list[Innings] = field(default_factory=list)
