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


@dataclass
class Match(DataClassJsonMixin):
    meta: Meta
    info: Info
