"""
class definitions for importing JSON match files
"""

from dataclasses import dataclass, field, fields
from datetime import date

from dataclasses_json import DataClassJsonMixin, config, dataclass_json


def date_field():
    return field(
        metadata=config(encoder=date.isoformat, decoder=date.fromisoformat),
        default=date(1900, 1, 1),
    )


def date_list_decoder(dts: list[str]) -> list[date]:
    return [date.fromisoformat(s) for s in dts]


@dataclass_json
@dataclass
class Meta:
    created: date = date_field()
    data_version: str = "0"
    revision: int = 0


@dataclass_json
@dataclass
class Event:
    name: str = ""
    stage: str = ""
    match_number: str = ""

    @property
    def as_string(self) -> str:
        return f"{self.name}|{self.stage or self.match_number}"


@dataclass_json
@dataclass
class Toss:
    decision: str = ""
    winner: str = ""


@dataclass_json
@dataclass
class Registry:
    people: dict[str, str] = field(default_factory=dict)


@dataclass_json
@dataclass
class Info:
    dates: list[date] = field(
        metadata=config(decoder=date_list_decoder), default_factory=list
    )
    balls_per_over: int = 0
    gender: str = ""
    match_type: str = ""
    match_type_number: int = 0
    overs: int = 0
    venue: str = ""
    toss: Toss = field(default_factory=Toss)
    registry: Registry = field(default_factory=Registry)
    event: Event = field(default_factory=Event)
    players: dict[str, list[str]] = field(default_factory=dict)
    teams: list[str] = field(default_factory=list)
    city: str = ""
    file_path: str = ""

    def database_fields(self) -> dict:
        return {
            "start_date": self.dates[0].isoformat(),
            "match_type": self.match_type,
            "match_type_number": self.match_type_number,
            "gender": self.gender,
            "venue": self.venue,
            "event": self.event.as_string,
            "city": self.city,
            "overs": self.overs,
            "balls_per_over": self.balls_per_over,
            "file_path": self.file_path,
        }

    def __repr__(self) -> str:
        return f"{self.dates[0]}: {self.match_type} {' vs '.join(self.teams)}"

    @property
    def selected_player_regs(self) -> list[dict[str, str]]:
        selections = [
            {
                "name": player,
                "reg": self.registry.people[player],
                "team": team,
            }
            for team, team_list in self.players.items()
            for player in team_list
        ]
        assert len(selections) == sum(
            len(team_list) for team_list in self.players.values()
        ), "mismatch between player lists and registry"
        return selections


@dataclass_json
@dataclass
class Extras:
    noballs: int = 0
    wides: int = 0
    legbyes: int = 0
    byes: int = 0

    @property
    def extra_type(self) -> str:
        try:
            res = next(
                field.name for field in fields(Extras) if self.__dict__[field.name] > 0
            )
        except StopIteration:
            return ""
        return res[:-1] if res else ""


@dataclass_json
@dataclass
class Runs:
    batter: int = 0
    extras: int = 0
    total: int = 0


@dataclass_json
@dataclass
class Dismissal:
    player_out: str = ""
    kind: str = ""

    def to_database_dismissal(self) -> dict:
        return {
            "dismissed": self.player_out,
            "how_out": self.kind,
        }


@dataclass
class Delivery(DataClassJsonMixin):
    ball_seq: int = 0
    legal_ball_seq: int = 0
    batter: str = ""
    bowler: str = ""
    non_striker: str = ""
    runs: Runs = field(default_factory=Runs)
    extras: Extras = field(default_factory=Extras)
    wickets: list[Dismissal] = field(default_factory=list)

    @property
    def is_bowler_extra(self) -> bool:
        return self.extras.extra_type in ["wide", "noball"]

    def to_database_ball(self) -> dict:
        return {
            "ball_seq": self.ball_seq,
            "ball": self.legal_ball_seq,
            "batter": self.batter,
            "bowled_by": self.bowler,
            "non_striker": self.non_striker,
            "batter_runs": self.runs.batter,
            "extra_runs": self.runs.extras,
            "extra_type": self.extras.extra_type,
            "wicket_fell": bool(self.wickets),
        } | (
            self.wickets[0].to_database_dismissal()
            if self.wickets
            else {
                "dismissed": "",
                "how_out": "",
            }
        )


@dataclass_json
@dataclass
class Over:
    over: int
    deliveries: list[Delivery] = field(
        default_factory=list, metadata=config(field_name="deliveries")
    )

    def __post_init__(self) -> None:
        legal_ball_seq = 0
        for ball_seq, deliv in enumerate(self.deliveries):
            deliv.ball_seq = ball_seq
            deliv.legal_ball_seq = legal_ball_seq
            if not deliv.is_bowler_extra:
                legal_ball_seq += 1

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


@dataclass
class Innings(DataClassJsonMixin):
    team: str = ""
    overs: list[Over] = field(default_factory=list)
    powerplays: list[PowerPlay] = field(default_factory=list)
    target: Target = field(default_factory=Target)

    def database_balls(self) -> list[dict]:
        return [
            {
                "over": over.over,
            }
            | deliv.to_database_ball()
            for over in self.overs
            for deliv in over.deliveries
        ]


@dataclass
class Match(DataClassJsonMixin):
    meta: Meta
    info: Info
    innings: list[Innings] = field(default_factory=list)


@dataclass
class Person:
    identifier: str
    name: str
    unique_name: str
    key_bcci: str = ""
    key_bcci_2: str = ""
    key_bigbash: str = ""
    key_cricbuzz: str = ""
    key_cricheroes: str = ""
    key_crichq: str = ""
    key_cricinfo: str = ""
    key_cricinfo_2: str = ""
    key_cricingif: str = ""
    key_cricketarchive: str = ""
    key_cricketarchive_2: str = ""
    key_nvplay: str = ""
    key_nvplay_2: str = ""
    key_opta: str = ""
    key_opta_2: str = ""
    key_pulse: str = ""
    key_pulse_2: str = ""
