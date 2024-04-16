from pathlib import Path

from app.ingest.classes import Match


def t20_dirs(gender: str, match_type: str):
    for p in Path("matches").glob(f"{gender}/{match_type}"):
        print(p)
        yield p


def t20_matches(gender: str = "*", match_type: str = "*") -> list[Match]:
    return [
        Match.from_json(p.read_text())
        for d in t20_dirs(gender, match_type)
        for p in d.glob("*.json")
    ]


class Statter:
    def __init__(self):
        self.accumulator = 0.0
        self.instance_count = 0

    def add(self, quantity):
        self.accumulator += quantity
        self.instance_count += 1

    @property
    def mean(self):
        return self.accumulator / self.instance_count
