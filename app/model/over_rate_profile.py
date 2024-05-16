from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path


def empty_t20_over_rates() -> dict[int, float]:
    # TOOD: what if there is *no* rate for a particular over?????
    # maybe make this a dict?
    return {}


@dataclass
class OverRateProfile:
    # maybe make this a list?
    # Perhaps interpolate for overs where there's no data?
    # or maybe better calculate the spread over base for the overs that are
    # present and interpolate from that.
    rates: dict[int, float] = field(default_factory=empty_t20_over_rates)

    def __sub__(self, other: OverRateProfile) -> OverRateProfile:
        return OverRateProfile(
            rates={i: self.rates[i] - other.rates[i] for i in range(20)}
        )

    def __add__(self, other: OverRateProfile) -> OverRateProfile:
        return OverRateProfile(
            rates={i: self.rates[i] + other.rates[i] for i in range(20)}
        )

    def __getitem__(self, idx: int) -> float:
        return self.rates[idx]

    def __setitem__(self, idx: int, value: float):
        self.rates[idx] = value

    def __len__(self) -> int:
        return len(self.rates)

    @classmethod
    def from_rows(cls, rows: list[sqlite3.Row]) -> OverRateProfile:
        prof = OverRateProfile()
        for row in rows:
            prof[row["over"]] = row["avg_runs"]
        return prof

    @classmethod
    def by_all(cls, db: sqlite3.Connection) -> OverRateProfile:
        sql = (Path(__file__).parent / "sql/base_first_inns_over_rates.sql").read_text()
        rows = db.execute(sql).fetchall()
        prof = cls.from_rows(rows)
        if len(prof) < 20:
            raise ValueError("must be 20 overs!")
        return prof

    @classmethod
    def by_player(cls, db: sqlite3.Connection, player_id: int) -> OverRateProfile:
        sql = (
            Path(__file__).parent / "sql/player_first_inns_over_rates.sql"
        ).read_text()
        rows = db.execute(sql, {"player_id": player_id}).fetchall()
        return cls.from_rows(rows)
